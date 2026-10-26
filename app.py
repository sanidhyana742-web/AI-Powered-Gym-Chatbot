from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import warnings
warnings.filterwarnings('ignore', category=FutureWarning)
import google.generativeai as genai
import json
import os
from datetime import datetime, timedelta
from functools import wraps
import base64
import cv2
import numpy as np

app = Flask(__name__)
app.secret_key = ""

# 🔑 Configure Gemini API
import os

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-3.8-flash")

# 📁 Database file paths
USERS_DB = "users_database.json"
CHAT_HISTORY_DB = "chat_history.json"
POSTURE_DB = "posture_analysis.json"
FITNESS_TIPS_DB = "fitness_tips.json"
PROGRESS_DB = "progress_tracker.json"
USER_PREFS_DB = "user_preferences.json"
ACHIEVEMENTS_DB = "achievements.json"
PERSONALITY_DB = "personality_preferences.json"
TRANSFORMATION_DB = "transformation_plans.json"

# ============= DATABASE FUNCTIONS =============

def load_users():
    """Load users from JSON database"""
    if os.path.exists(USERS_DB):
        with open(USERS_DB, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    """Save users to JSON database"""
    with open(USERS_DB, 'w') as f:
        json.dump(users, f, indent=4)

def load_chat_history():
    """Load chat history from JSON database"""
    if os.path.exists(CHAT_HISTORY_DB):
        with open(CHAT_HISTORY_DB, 'r') as f:
            return json.load(f)
    return {}

def save_chat_history(history):
    """Save chat history to JSON database"""
    with open(CHAT_HISTORY_DB, 'w') as f:
        json.dump(history, f, indent=4)

def load_posture_data():
    """Load posture analysis data from JSON database"""
    if os.path.exists(POSTURE_DB):
        with open(POSTURE_DB, 'r') as f:
            return json.load(f)
    return {}

def save_posture_data(data):
    """Save posture analysis data to JSON database"""
    with open(POSTURE_DB, 'w') as f:
        json.dump(data, f, indent=4)

def load_fitness_tips():
    """Load fitness tips from JSON database"""
    if os.path.exists(FITNESS_TIPS_DB):
        with open(FITNESS_TIPS_DB, 'r') as f:
            return json.load(f)
    return {}

def save_fitness_tips(data):
    """Save fitness tips to JSON database"""
    with open(FITNESS_TIPS_DB, 'w') as f:
        json.dump(data, f, indent=4)

def load_progress():
    """Load user progress from JSON database"""
    if os.path.exists(PROGRESS_DB):
        with open(PROGRESS_DB, 'r') as f:
            return json.load(f)
    return {}

def save_progress(data):
    """Save user progress to JSON database"""
    with open(PROGRESS_DB, 'w') as f:
        json.dump(data, f, indent=4)

def load_user_preferences():
    """Load user preferences from JSON database"""
    if os.path.exists(USER_PREFS_DB):
        with open(USER_PREFS_DB, 'r') as f:
            return json.load(f)
    return {}

def save_user_preferences(data):
    """Save user preferences to JSON database"""
    with open(USER_PREFS_DB, 'w') as f:
        json.dump(data, f, indent=4)

def load_achievements():
    """Load achievements from JSON database"""
    if os.path.exists(ACHIEVEMENTS_DB):
        with open(ACHIEVEMENTS_DB, 'r') as f:
            return json.load(f)
    return {}

def save_achievements(data):
    """Save achievements to JSON database"""
    with open(ACHIEVEMENTS_DB, 'w') as f:
        json.dump(data, f, indent=4)

def load_personality_preferences():
    """Load personality preferences from JSON database"""
    if os.path.exists(PERSONALITY_DB):
        with open(PERSONALITY_DB, 'r') as f:
            return json.load(f)
    return {}

def save_personality_preferences(data):
    """Save personality preferences to JSON database"""
    with open(PERSONALITY_DB, 'w') as f:
        json.dump(data, f, indent=4)

def load_transformation_plans():
    """Load transformation plans from JSON database"""
    if os.path.exists(TRANSFORMATION_DB):
        with open(TRANSFORMATION_DB, 'r') as f:
            return json.load(f)
    return {}

def save_transformation_plans(data):
    """Save transformation plans to JSON database"""
    with open(TRANSFORMATION_DB, 'w') as f:
        json.dump(data, f, indent=4)

# ============= AUTHENTICATION =============

def login_required(f):
    """Decorator to check if user is logged in"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({"error": "Not logged in"}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route("/register", methods=["POST"])
def register():
    """Register a new user"""
    data = request.json
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")
    
    users = load_users()
    
    if username in users:
        return jsonify({"success": False, "message": "Username already exists"}), 400
    
    users[username] = {
        "password": password,
        "email": email,
        "age": 0,
        "weight": 0,
        "height": 0,
        "goal": "general fitness",
        "activity_level": "moderate",
        "created_at": datetime.now().isoformat()
    }
    
    save_users(users)
    return jsonify({"success": True, "message": "User registered successfully"}), 201

@app.route("/login", methods=["POST"])
def login():
    """Login user"""
    data = request.json
    username = data.get("username")
    password = data.get("password")
    
    users = load_users()
    
    if username not in users or users[username]["password"] != password:
        return jsonify({"success": False, "message": "Invalid credentials"}), 401
    
    session['user_id'] = username
    return jsonify({"success": True, "message": "Logged in successfully"}), 200

@app.route("/logout")
def logout():
    """Logout user"""
    session.pop('user_id', None)
    return redirect("/")

@app.route("/check-auth")
def check_auth():
    """Check if user is authenticated"""
    if 'user_id' in session:
        return jsonify({"authenticated": True, "username": session['user_id']}), 200
    return jsonify({"authenticated": False}), 200

# ============= USER PROFILE =============

@app.route("/update-profile", methods=["POST"])
@login_required
def update_profile():
    """Update user profile information"""
    data = request.json
    username = session['user_id']
    users = load_users()
    
    if username in users:
        users[username].update({
            "age": int(data.get("age", 0)),
            "weight": float(data.get("weight", 0)),
            "height": float(data.get("height", 0)),
            "goal": data.get("goal", "general fitness"),
            "activity_level": data.get("activity_level", "moderate")
        })
        save_users(users)
        return jsonify({"success": True, "message": "Profile updated"}), 200
    
    return jsonify({"success": False, "message": "User not found"}), 404

@app.route("/get-profile")
@login_required
def get_profile():
    """Get user profile information"""
    username = session['user_id']
    users = load_users()
    
    if username in users:
        return jsonify(users[username]), 200
    return jsonify({"success": False}), 404

# ============= CALORIE CALCULATOR =============

@app.route("/calculate-calories", methods=["POST"])
def calculate_calories():
    """Calculate daily calorie needs using Harris-Benedict equation"""
    data = request.json
    age = int(data.get("age", 30))
    weight = float(data.get("weight", 70))  # kg
    height = float(data.get("height", 170))  # cm
    gender = data.get("gender", "male")
    activity_level = float(data.get("activity_level", 1.55))
    
    # Harris-Benedict Equation
    if gender.lower() == "male":
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    
    tdee = bmr * activity_level
    
    # Calculate macros (40% carbs, 30% protein, 30% fat)
    protein_calories = tdee * 0.30
    carbs_calories = tdee * 0.40
    fat_calories = tdee * 0.30
    
    return jsonify({
        "bmr": round(bmr, 2),
        "tdee": round(tdee, 2),
        "macros": {
            "protein_g": round(protein_calories / 4, 2),
            "carbs_g": round(carbs_calories / 4, 2),
            "fat_g": round(fat_calories / 9, 2)
        }
    }), 200

@app.route("/calculate-bmi", methods=["POST"])
def calculate_bmi():
    """Calculate BMI and give recommendations"""
    data = request.json
    weight = float(data.get("weight", 70))  # kg
    height = float(data.get("height", 170))  # cm
    
    height_m = height / 100
    bmi = weight / (height_m ** 2)
    
    if bmi < 18.5:
        category = "Underweight"
        advice = "Consider consulting a nutritionist for healthy weight gain"
    elif bmi < 25:
        category = "Normal weight"
        advice = "Maintain your current healthy lifestyle"
    elif bmi < 30:
        category = "Overweight"
        advice = "Focus on balanced diet and regular exercise"
    else:
        category = "Obese"
        advice = "Consult a healthcare professional and start a fitness plan"
    
    return jsonify({
        "bmi": round(bmi, 2),
        "category": category,
        "advice": advice
    }), 200

# ============= AI CHAT WITH MEMORY =============

@app.route("/chat", methods=["POST"])
def chat():
    """Chat with AI fitness coach with memory"""
    data = request.json
    user_message = data.get("message")
    username = session.get('user_id', 'guest')
    
    # Get user profile if logged in
    user_profile = ""
    if username != 'guest':
        users = load_users()
        if username in users:
            profile = users[username]
            user_profile = f"""
User Profile:
- Age: {profile.get('age', 'Not set')}
- Weight: {profile.get('weight', 'Not set')} kg
- Height: {profile.get('height', 'Not set')} cm
- Goal: {profile.get('goal', 'general fitness')}
- Activity Level: {profile.get('activity_level', 'moderate')}
"""
    
    # Create context-aware prompt
    system_prompt = f"""You are a professional fitness coach with expertise in:
- Personalized fitness plans
- Nutrition and meal planning
- Calorie management
- Motivational coaching
- Injury prevention

{user_profile}

Respond with practical, actionable advice. Format your response with clear sections and relevant emojis."""
    
    full_prompt = f"{system_prompt}\n\nUser: {user_message}"
    
    try:
        response = model.generate_content(full_prompt)
        
        # Store message in history
        history = load_chat_history()
        if username not in history:
            history[username] = []
        
        history[username].append({
            "timestamp": datetime.now().isoformat(),
            "user": user_message,
            "assistant": response.text
        })
        save_chat_history(history)
        
        return jsonify({"response": response.text}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/get-chat-history")
@login_required
def get_chat_history():
    """Get user's chat history"""
    username = session['user_id']
    history = load_chat_history()
    
    user_history = history.get(username, [])
    return jsonify({"history": user_history}), 200

@app.route("/clear-chat-history", methods=["POST"])
@login_required
def clear_chat_history():
    """Clear user's chat history"""
    username = session['user_id']
    history = load_chat_history()
    
    if username in history:
        history[username] = []
        save_chat_history(history)
    
    return jsonify({"success": True}), 200

# ============= GOAL-BASED AI RESPONSES =============

@app.route("/goal-based-response", methods=["POST"])
def goal_based_response():
    """Generate goal-specific AI responses"""
    data = request.json
    goal = data.get("goal", "general fitness")
    question = data.get("question")
    
    goal_prompts = {
        "weight loss": "You are a weight loss specialist. Focus on calorie deficit, cardio, healthy eating.",
        "muscle gain": "You are a strength training coach. Focus on progressive overload, protein, hypertrophy.",
        "endurance": "You are an endurance coach. Focus on sustained effort, cardio capacity, stamina.",
        "general fitness": "You are a general fitness coach. Focus on balanced training and overall health."
    }
    
    system_prompt = goal_prompts.get(goal, goal_prompts["general fitness"])
    
    prompt = f"{system_prompt}\n\nAnswer this question: {question}"
    
    response = model.generate_content(prompt)
    return jsonify({"response": response.text}), 200

# ============= FITNESS DASHBOARD DATA =============

@app.route("/get-dashboard-data")
@login_required
def get_dashboard_data():
    """Get fitness dashboard statistics"""
    username = session['user_id']
    users = load_users()
    history = load_chat_history()
    
    if username not in users:
        return jsonify({"error": "User not found"}), 404
    
    profile = users[username]
    user_history = history.get(username, [])
    
    # Calculate statistics
    dashboard_data = {
        "profile": profile,
        "stats": {
            "total_chats": len(user_history),
            "member_since": profile.get("created_at", ""),
            "goal": profile.get("goal", ""),
            "current_weight": profile.get("weight", 0),
            "target_weight": profile.get("weight", 0) - 5  # Example target
        },
        "recent_conversations": user_history[-5:] if user_history else []
    }
    
    return jsonify(dashboard_data), 200



# ============= POSTURE DETECTION =============

def calculate_angle(a, b, c):
    """Calculate angle between three points"""
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    
    if angle > 180.0:
        angle = 360 - angle
    
    return angle

def analyze_posture(img_rgb):
    """Analyze posture using body contour detection (no MediaPipe needed)"""
    posture_score = 100
    feedback = []
    issues = []
    
    try:
        # Convert to HSV for skin detection
        img_hsv = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2HSV)
        
        # Define skin color range (works for most skin tones)
        lower_skin = np.array([0, 20, 70], dtype=np.uint8)
        upper_skin = np.array([20, 255, 255], dtype=np.uint8)
        skin_mask = cv2.inRange(img_hsv, lower_skin, upper_skin)
        
        # Also check yellow-orange range
        lower_skin2 = np.array([10, 50, 60], dtype=np.uint8)
        upper_skin2 = np.array([25, 200, 255], dtype=np.uint8)
        skin_mask2 = cv2.inRange(img_hsv, lower_skin2, upper_skin2)
        
        skin_mask = cv2.bitwise_or(skin_mask, skin_mask2)
        
        # Morphological operations to clean up
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        skin_mask = cv2.morphologyEx(skin_mask, cv2.MORPH_CLOSE, kernel)
        skin_mask = cv2.morphologyEx(skin_mask, cv2.MORPH_OPEN, kernel)
        
        # Find contours
        contours, _ = cv2.findContours(skin_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if len(contours) == 0:
            return {
                "score": 0,
                "overall": "No person detected",
                "feedback": ["Make sure you're clearly visible"],
                "issues": ["Camera positioning: Ensure full body is in frame"],
                "timestamp": datetime.now().isoformat()
            }
        
        # Find largest contour (body)
        body_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(body_contour)
        
        # Analyze body shape
        img_height, img_width = img_rgb.shape[:2]
        
        # 1. Check verticality (spine alignment)
        # Wide/narrow ratio indicates posture
        aspect_ratio = h / w if w > 0 else 0
        if aspect_ratio < 1.5:  # Hunched/leaning posture
            posture_score -= 25
            issues.append("Spine misalignment - appear hunched or leaning")
        else:
            feedback.append("✓ Spine appears well aligned")
        
        # 2. Check centering (not leaning to sides)
        body_center_x = x + w / 2
        img_center_x = img_width / 2
        lean_ratio = abs(body_center_x - img_center_x) / img_width
        
        if lean_ratio > 0.15:  # Leaning to one side
            posture_score -= 20
            issues.append("Body leaning - stand more upright and centered")
        else:
            feedback.append("✓ Good body centering")
        
        # 3. Check shoulder symmetry by analyzing top part of contour
        top_part = body_contour[body_contour[:, 0, 1] < y + h * 0.3]
        if len(top_part) > 0:
            top_x_coords = top_part[:, 0, 0]
            left_edge = np.min(top_x_coords)
            right_edge = np.max(top_x_coords)
            shoulder_diff = abs((x + w / 2 - left_edge) - (right_edge - (x + w / 2)))
            
            if shoulder_diff > w * 0.1:
                posture_score -= 15
                issues.append("Uneven shoulders - align shoulders level")
            else:
                feedback.append("✓ Shoulders appear level")
        
        # 4. Check head position (top contour concentration)
        head_region = body_contour[body_contour[:, 0, 1] < y + h * 0.2]
        if len(head_region) > 0:
            head_left = np.min(head_region[:, 0, 0])
            head_right = np.max(head_region[:, 0, 0])
            head_center = (head_left + head_right) / 2
            body_center = x + w / 2
            
            head_offset = abs(head_center - body_center)
            if head_offset > w * 0.08:
                posture_score -= 20
                issues.append("Head leaning forward - keep head over shoulders")
            else:
                feedback.append("✓ Head position is neutral")
        
        # 5. Check overall posture confidence
        contour_area = cv2.contourArea(body_contour)
        image_area = img_height * img_width
        coverage = contour_area / image_area
        
        if coverage < 0.05:  # Person too small/far
            posture_score -= 10
            issues.append("Position closer to camera for better analysis")
        
        posture_score = max(0, min(100, posture_score))
        
        if posture_score >= 85:
            overall = "Excellent posture! ✅"
        elif posture_score >= 70:
            overall = "Good posture - minor adjustments needed"
        elif posture_score >= 50:
            overall = "Fair posture - multiple adjustments recommended"
        else:
            overall = "Poor posture - significant adjustments needed"
        
        if not feedback:
            feedback.append("✓ Overall posture looks good")
        
        if not issues:
            issues.append("No major issues detected")
        
        return {
            "score": posture_score,
            "overall": overall,
            "feedback": feedback,
            "issues": issues,
            "timestamp": datetime.now().isoformat(),
            "method": "Advanced body contour analysis"
        }
    
    except Exception as e:
        return {
            "score": 0,
            "overall": "Analysis error",
            "feedback": [],
            "issues": [f"Error: {str(e)}"],
            "timestamp": datetime.now().isoformat()
        }

@app.route("/analyze-posture", methods=["POST"])
@login_required
def analyze_posture_endpoint():
    """Analyze posture from base64 encoded image"""
    data = request.json
    img_data = data.get("image")
    
    if not img_data:
        return jsonify({"error": "No image provided"}), 400
    
    try:
        # Decode base64 image
        img_bytes = base64.b64decode(img_data.split(',')[1])
        nparr = np.frombuffer(img_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            return jsonify({"error": "Invalid image data"}), 400
        
        # Convert to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Analyze posture using contour-based method (no MediaPipe needed)
        analysis = analyze_posture(image_rgb)
        
        # Save to history
        username = session.get('user_id', 'guest')
        posture_data = load_posture_data()
        
        if username not in posture_data:
            posture_data[username] = []
        
        posture_data[username].append(analysis)
        save_posture_data(posture_data)
        
        return jsonify(analysis), 200
    
    except Exception as e:
        return jsonify({"error": str(e), "overall": "Analysis failed", "score": 0}), 500

@app.route("/get-posture-history")
@login_required
def get_posture_history():
    """Get user's posture analysis history"""
    username = session['user_id']
    posture_data = load_posture_data()
    
    user_history = posture_data.get(username, [])
    return jsonify({"history": user_history[-10:]}), 200

@app.route("/clear-posture-history", methods=["POST"])
@login_required
def clear_posture_history():
    """Clear user's posture history"""
    username = session['user_id']
    posture_data = load_posture_data()
    
    if username in posture_data:
        posture_data[username] = []
        save_posture_data(posture_data)
    
    return jsonify({"success": True}), 200

# ============= NEW FEATURES =============

# 1. DAILY FITNESS TIPS WITH AUTO-UPDATE

@app.route("/get-daily-tips")
def get_daily_tips():
    """Get daily fitness tips that auto-update"""
    today = datetime.now().strftime("%Y-%m-%d")
    tips_data = load_fitness_tips()
    
    # Check if we have today's tips
    if today in tips_data:
        return jsonify({"tips": tips_data[today], "date": today}), 200
    
    # Generate new tips for today
    prompt = """Generate 5 unique and motivating daily fitness tips for today. 
    Each tip should be:
    - Short and actionable (max 1 sentence)
    - Different focus (cardio, strength, flexibility, nutrition, mental health)
    - Include an emoji at the start
    
    Format as a JSON array of strings."""
    
    try:
        response = model.generate_content(prompt)
        import re
        # Extract JSON from response
        json_match = re.search(r'\[.*\]', response.text, re.DOTALL)
        if json_match:
            tips = eval(json_match.group())
        else:
            tips = response.text.split('\n')
        
        tips_data[today] = tips
        save_fitness_tips(tips_data)
        
        return jsonify({"tips": tips, "date": today, "fresh": True}), 200
    except Exception as e:
        return jsonify({"error": str(e), "tips": ["Stay hydrated!", "Stretch daily!", "Move more!"]}), 200

# 2. SMART SUGGESTION AUTO BUTTON

@app.route("/get-smart-suggestion", methods=["POST"])
@login_required
def get_smart_suggestion():
    """Get AI-powered smart fitness suggestion based on user profile"""
    username = session['user_id']
    users = load_users()
    
    if username not in users:
        return jsonify({"error": "User not found"}), 404
    
    profile = users[username]
    
    prompt = f"""Based on this user's fitness profile:
    - Goal: {profile.get('goal', 'general fitness')}
    - Age: {profile.get('age', 'Not set')}
    - Weight: {profile.get('weight', 'Not set')} kg
    - Activity Level: {profile.get('activity_level', 'moderate')}
    
    Provide ONE specific, actionable fitness suggestion for RIGHT NOW. 
    Make it practical and motivating. Include:
    1. The suggestion
    2. Why it's good for them
    3. How to do it (1-2 sentences)
    
    Format with emojis and clear sections."""
    
    try:
        response = model.generate_content(prompt)
        return jsonify({"suggestion": response.text, "timestamp": datetime.now().isoformat()}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 3. PROGRESS TRACKER

@app.route("/log-progress", methods=["POST"])
@login_required
def log_progress():
    """Log fitness progress (weight, workouts, etc)"""
    username = session['user_id']
    data = request.json
    
    progress = load_progress()
    if username not in progress:
        progress[username] = []
    
    progress_entry = {
        "date": datetime.now().isoformat(),
        "type": data.get("type"),  # weight, workout_completed, distance, etc
        "value": data.get("value"),
        "notes": data.get("notes", "")
    }
    
    progress[username].append(progress_entry)
    save_progress(progress)
    
    return jsonify({"success": True, "message": "Progress logged"}), 200

@app.route("/get-progress")
@login_required
def get_user_progress():
    """Get user's progress data with analytics"""
    username = session['user_id']
    progress = load_progress()
    user_progress = progress.get(username, [])
    
    # Calculate statistics
    weight_logs = [p for p in user_progress if p["type"] == "weight"]
    workout_count = len([p for p in user_progress if p["type"] == "workout_completed"])
    
    stats = {
        "total_entries": len(user_progress),
        "workouts_completed": workout_count,
        "weight_logs": len(weight_logs),
        "recent_entries": user_progress[-10:],
    }
    
    if weight_logs:
        weights = [float(p["value"]) for p in weight_logs]
        stats["weight_change"] = weights[-1] - weights[0]
        stats["current_weight"] = weights[-1]
        stats["starting_weight"] = weights[0]
    
    return jsonify(stats), 200

@app.route("/get-progress-chart")
@login_required
def get_progress_chart():
    """Get progress data formatted for charts"""
    username = session['user_id']
    progress = load_progress()
    user_progress = progress.get(username, [])
    
    weight_logs = [p for p in user_progress if p["type"] == "weight"]
    weight_logs_sorted = sorted(weight_logs, key=lambda x: x["date"])
    
    chart_data = {
        "dates": [p["date"][:10] for p in weight_logs_sorted],
        "weights": [float(p["value"]) for p in weight_logs_sorted],
        "labels": [p.get("notes", "") for p in weight_logs_sorted]
    }
    
    return jsonify(chart_data), 200

# 4. FITNESS MOTIVATION GENERATOR

@app.route("/get-motivation")
@login_required
def get_motivation():
    """Get personalized motivational message"""
    username = session['user_id']
    users = load_users()
    
    if username not in users:
        return jsonify({"error": "User not found"}), 404
    
    profile = users[username]
    
    prompt = f"""Generate a SHORT (2-3 sentences), highly personalized motivational message for a fitness enthusiast with:
    - Goal: {profile.get('goal', 'general fitness')}
    - Activity Level: {profile.get('activity_level', 'moderate')}
    
    Make it powerful, action-oriented, and specific to their goals. Include an inspirational emoji."""
    
    try:
        response = model.generate_content(prompt)
        return jsonify({
            "motivation": response.text,
            "timestamp": datetime.now().isoformat()
        }), 200
    except Exception as e:
        return jsonify({"motivation": "💪 You've got this! Every rep counts!"}), 200

# 5. USER PREFERENCES (DARK/LIGHT MODE, PROFILE MEMORY)

@app.route("/set-preferences", methods=["POST"])
@login_required
def set_preferences():
    """Save user preferences"""
    username = session['user_id']
    data = request.json
    
    prefs = load_user_preferences()
    if username not in prefs:
        prefs[username] = {}
    
    prefs[username].update({
        "theme": data.get("theme", "dark"),
        "notifications": data.get("notifications", True),
        "auto_tips": data.get("auto_tips", True),
        "goal_reminders": data.get("goal_reminders", True),
        "language": data.get("language", "en"),
        "updated_at": datetime.now().isoformat()
    })
    
    save_user_preferences(prefs)
    return jsonify({"success": True, "message": "Preferences saved"}), 200

@app.route("/get-preferences")
@login_required
def get_preferences():
    """Get user preferences"""
    username = session['user_id']
    prefs = load_user_preferences()
    
    user_prefs = prefs.get(username, {
        "theme": "dark",
        "notifications": True,
        "auto_tips": True,
        "goal_reminders": True,
        "language": "en"
    })
    
    return jsonify(user_prefs), 200

# 6. PROFILE MEMORY (EXTENDED USER INFO)

@app.route("/save-profile-memory", methods=["POST"])
@login_required
def save_profile_memory():
    """Save extended user profile information for memory"""
    username = session['user_id']
    data = request.json
    users = load_users()
    
    if username in users:
        # Add memory fields
        users[username].update({
            "favorite_exercises": data.get("favorite_exercises", []),
            "dietary_restrictions": data.get("dietary_restrictions", []),
            "injury_history": data.get("injury_history", []),
            "availability": data.get("availability", "anytime"),
            "preferred_workout_type": data.get("preferred_workout_type", "mixed"),
            "past_goals": data.get("past_goals", []),
            "motivational_keywords": data.get("motivational_keywords", []),
            "profile_memory_updated": datetime.now().isoformat()
        })
        save_users(users)
        return jsonify({"success": True, "message": "Profile memory saved"}), 200
    
    return jsonify({"error": "User not found"}), 404

@app.route("/get-full-profile")
@login_required
def get_full_profile():
    """Get complete user profile including memory fields"""
    username = session['user_id']
    users = load_users()
    
    if username in users:
        return jsonify(users[username]), 200
    return jsonify({"error": "User not found"}), 404

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/chatpage")
def chatpage():
    if 'user_id' not in session:
        return redirect("/auth")
    return render_template("chat.html")

@app.route("/auth")
def auth_page():
    return render_template("auth.html")

@app.route("/dashboard")
def dashboard():
    if 'user_id' not in session:
        return redirect("/auth")
    return render_template("dashboard.html")

@app.route("/workout-timer")
def workout_timer():
    return render_template("workout-timer.html")

@app.route("/calculator")
def calculator():
    return render_template("calculator.html")

@app.route("/posture")
def posture():
    if 'user_id' not in session:
        return redirect("/auth")
    return render_template("posture.html")

@app.route("/meal-plan")
def meal_plan():
    if 'user_id' not in session:
        return redirect("/auth")
    return render_template("meal-plan.html")

@app.route("/generate-meal-plan", methods=['POST'])
def generate_meal_plan():
    try:
        data = request.json
        goal = data.get('fitness_goal', 'general fitness')
        dietary_type = data.get('dietary_type', 'mixed')
        servings = int(data.get('servings', 1))
        
        prompt = f"""Generate a detailed meal plan for one day with breakfast, lunch, and dinner for someone with the following:
- Fitness Goal: {goal}
- Dietary Type: {dietary_type}
- Servings: {servings} person(s)

For each meal, provide:
1. Meal name
2. 4-5 key ingredients/items
3. Estimated calories
4. Macros breakdown (Protein, Carbs, Fats)

Format your response as JSON with keys "breakfast", "lunch", "dinner". Each meal should have:
{{"name": "", "items": ["item1", "item2", ...], "calories": "XXX", "macros": "Protein XXg, Carbs XXg, Fats XXg"}}

Make the meals appropriate for {goal.lower()} and ensure they are {dietary_type.lower()}."""

        response = model.generate_content(prompt)
        response_text = response.text
        
        # Clean up the response
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0]
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0]
        
        meal_data = json.loads(response_text.strip())
        return jsonify(meal_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/generate-single-meal", methods=['POST'])
def generate_single_meal():
    try:
        data = request.json
        meal_type = data.get('meal_type', 'lunch')
        goal = data.get('fitness_goal', 'general fitness')
        dietary_type = data.get('dietary_type', 'mixed')
        servings = int(data.get('servings', 1))
        
        prompt = f"""Generate a detailed {meal_type} meal plan for someone with the following:
- Fitness Goal: {goal}
- Dietary Type: {dietary_type}
- Servings: {servings} person(s)

Provide:
1. A delicious {meal_type} meal name
2. 5-7 key ingredients/items with quantities
3. Estimated calories
4. Macros breakdown (Protein, Carbs, Fats)
5. Simple cooking instructions

Format your response as JSON with the following structure:
{{"name": "", "items": ["item1 with quantity", "item2 with quantity", ...], "calories": "XXX", "macros": "Protein XXg, Carbs XXg, Fats XXg", "instructions": "Step 1: ... Step 2: ..."}}

Make the meal appropriate for {goal.lower()} and ensure it is {dietary_type.lower()}."""

        response = model.generate_content(prompt)
        response_text = response.text
        
        # Clean up the response
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0]
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0]
        
        meal_data = json.loads(response_text.strip())
        return jsonify(meal_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/workout")
def workout():
    if 'user_id' not in session:
        return redirect("/auth")
    return render_template("workout.html")

@app.route("/personality-mode")
def personality_mode():
    if 'user_id' not in session:
        return redirect("/auth")
    return render_template("personality-mode.html")

@app.route("/transformation-plan")
def transformation_plan():
    if 'user_id' not in session:
        return redirect("/auth")
    return render_template("transformation-plan.html")

@app.route("/mood-workout")
def mood_workout():
    if 'user_id' not in session:
        return redirect("/auth")
    return render_template("mood-workout.html")

@app.route("/achievements")
def achievements():
    if 'user_id' not in session:
        return redirect("/auth")
    return render_template("achievements.html")

@app.route("/generate-workout", methods=['POST'])
def generate_workout():
    try:
        data = request.json
        goal = data.get('fitness_goal', 'general fitness')
        duration = data.get('duration', '60')
        equipment = data.get('equipment', 'no equipment')
        intensity = data.get('intensity', 'intermediate')
        
        prompt = f"""Generate a detailed {duration}-minute workout plan for someone with the following:
- Fitness Goal: {goal}
- Equipment Available: {equipment}
- Intensity Level: {intensity}

Provide a structured workout with:
1. Workout name (catchy and motivating)
2. Main focus areas
3. Warm-up (2-3 minutes)
4. List of 6-10 exercises with:
   - Exercise name
   - Sets x Reps
   - Rest time between sets
   - Detailed instructions
5. Cool-down (2-3 minutes)

Format your response as JSON with the following structure:
{{
  "workout_name": "",
  "duration": "{duration} minutes",
  "intensity": "{intensity}",
  "focus": "",
  "warmup": "",
  "exercises": [
    {{"name": "", "sets_reps": "", "rest": "", "instructions": ""}},
    ...
  ],
  "cooldown": ""
}}

Make sure the workout is appropriate for {goal.lower()} and uses only {equipment.lower()}. The workout should take approximately {duration} minutes."""

        response = model.generate_content(prompt)
        response_text = response.text
        
        # Clean up the response
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0]
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0]
        
        workout_data = json.loads(response_text.strip())
        return jsonify(workout_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/chat-with-bot", methods=['POST'])
def chat_with_bot():
    try:
        data = request.json
        user_message = data.get('message', '')
        chat_history = data.get('chat_history', [])
        
        # Build conversation context
        conv_context = ""
        for msg in chat_history[-5:]:  # Last 5 messages for context
            role = "User" if msg['role'] == 'user' else "Assistant"
            conv_context += f"{role}: {msg['content']}\n"
        
        prompt = f"""You are FitnessAI, a knowledgeable and friendly fitness chatbot. 
You help users with workout advice, exercise tips, nutrition guidance, fitness goals, and any health-related questions.
Be encouraging, specific, and provide practical advice.

Conversation history:
{conv_context}

User: {user_message}

Provide a helpful, friendly response. Keep it concise (1-2 sentences)."""

        response = model.generate_content(prompt)
        bot_reply = response.text.strip()
        
        return jsonify({"reply": bot_reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# ============= NEW FEATURE 1: AI FITNESS PERSONALITY MODE =============

@app.route("/set-ai-personality", methods=["POST"])
@login_required
def set_ai_personality():
    """Set user's preferred AI fitness personality"""
    username = session['user_id']
    data = request.json
    personality = data.get("personality", "friendly")  # friendly, strict, motivational, scientific, chill
    
    personalities = load_personality_preferences()
    if username not in personalities:
        personalities[username] = {}
    
    personalities[username]["type"] = personality
    personalities[username]["updated_at"] = datetime.now().isoformat()
    save_personality_preferences(personalities)
    
    return jsonify({"success": True, "personality": personality, "message": "AI personality updated"}), 200

@app.route("/get-ai-personality")
@login_required
def get_ai_personality():
    """Get user's AI fitness personality preference"""
    username = session['user_id']
    personalities = load_personality_preferences()
    
    user_personality = personalities.get(username, {}).get("type", "friendly")
    
    personality_descriptions = {
        "friendly": "💬 A supportive friend who motivates you with encouragement",
        "strict": "💪 A tough coach who pushes you to your limits",
        "motivational": "🔥 An inspirational speaker who hypes you up",
        "scientific": "🧬 A fitness scientist who explains everything with data",
        "chill": "😎 A relaxed buddy who keeps fitness fun and easy"
    }
    
    return jsonify({
        "personality": user_personality,
        "description": personality_descriptions.get(user_personality, "")
    }), 200

@app.route("/get-personalized-response", methods=["POST"])
@login_required
def get_personalized_response():
    """Get AI response with user's preferred personality"""
    username = session['user_id']
    data = request.json
    message = data.get("message")
    
    personalities = load_personality_preferences()
    personality = personalities.get(username, {}).get("type", "friendly")
    
    personality_prompts = {
        "friendly": "You are an encouraging and supportive fitness friend. Use warm language, compliments, and makes fitness feel achievable.",
        "strict": "You are a tough drill sergeant fitness coach. Be direct, demanding, and push the user to give their all. No excuses!",
        "motivational": "You are a hyperenergetic motivational speaker. Use excitement, powerful language, and inspire people to achieve greatness.",
        "scientific": "You are a fitness scientist. Explain everything with data, studies, and scientific accuracy. Use technical terms.",
        "chill": "You are a laid-back fitness buddy. Keep it fun, relaxed, and make fitness enjoyable without being preachy."
    }
    
    system_prompt = personality_prompts.get(personality, personality_prompts["friendly"])
    
    prompt = f"{system_prompt}\n\nUser message: {message}\n\nRespond in character with your unique personality."
    
    try:
        response = model.generate_content(prompt)
        return jsonify({"response": response.text, "personality": personality}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ============= NEW FEATURE 2: AI BODY TRANSFORMATION PLAN =============

@app.route("/generate-transformation-plan", methods=["POST"])
@login_required
def generate_transformation_plan():
    """Generate comprehensive body transformation plan"""
    username = session['user_id']
    data = request.json
    
    current_weight = float(data.get("current_weight", 70))
    target_weight = float(data.get("target_weight", 70))
    weeks = int(data.get("weeks", 12))
    goal = data.get("goal", "weight loss")
    fitness_level = data.get("fitness_level", "intermediate")
    
    prompt = f"""Create a detailed {weeks}-week body transformation plan for:
- Current Weight: {current_weight} kg
- Target Weight: {target_weight} kg
- Goal: {goal}
- Fitness Level: {fitness_level}

Provide a JSON response with:
1. weekly_breakdown: Array of {weeks} weeks with milestone targets
2. nutrition_plan: Daily macro targets and meal frequency
3. workout_plan: Weekly exercise structure (days per week, focus areas)
4. timeline: Key milestones and checkpoints
5. supplements: Optional supplements to consider
6. tips: 5 key behavioral tips for success

Format as JSON with clear structure. Make it realistic and science-based."""

    try:
        response = model.generate_content(prompt)
        response_text = response.text
        
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0]
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0]
        
        plan = json.loads(response_text.strip())
        
        # Save the plan
        plans = load_transformation_plans()
        if username not in plans:
            plans[username] = []
        
        plan_entry = {
            "plan_id": len(plans[username]) + 1,
            "created_at": datetime.now().isoformat(),
            "current_weight": current_weight,
            "target_weight": target_weight,
            "weeks": weeks,
            "goal": goal,
            "plan_details": plan
        }
        
        plans[username].append(plan_entry)
        save_transformation_plans(plans)
        
        return jsonify({
            "success": True,
            "plan": plan,
            "plan_id": plan_entry["plan_id"],
            "message": f"Transformation plan created for {weeks} weeks!"
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/get-transformation-plans")
@login_required
def get_transformation_plans():
    """Get user's transformation plans"""
    username = session['user_id']
    plans = load_transformation_plans()
    
    user_plans = plans.get(username, [])
    return jsonify({"plans": user_plans, "total": len(user_plans)}), 200

# ============= NEW FEATURE 3: MOOD-BASED WORKOUT =============

MOOD_WORKOUTS = {
    "energetic": "High-intensity interval training with max energy and power",
    "demotivated": "Light, fun workout with achievable goals and positive vibes",
    "stressed": "Calming yoga and stretching to release tension",
    "angry": "Heavy strength training to channel intensity productively",
    "tired": "Low-impact recovery workout with gentle movement",
    "confident": "Advanced challenging workout to test your limits",
    "anxious": "Steady-state cardio to calm nerves and focus",
    "bored": "Fun, varied workout with different exercises to stay entertained"
}

@app.route("/get-mood-workout", methods=["POST"])
@login_required
def get_mood_workout():
    """Generate workout based on user's current mood"""
    data = request.json
    mood = data.get("mood", "energetic").lower()
    duration = data.get("duration", "30")
    equipment = data.get("equipment", "no equipment")
    
    mood_description = MOOD_WORKOUTS.get(mood, MOOD_WORKOUTS["energetic"])
    
    prompt = f"""Create a {duration}-minute workout specifically designed for someone who is feeling {mood}.
    
    Mood Context: {mood_description}
    Equipment: {equipment}
    
    Generate a workout that:
    1. Addresses the emotional/physical state of the mood
    2. Provides appropriate intensity level
    3. Includes motivation tips for this mood
    
    Format as JSON with:
    {{
      "workout_name": "Creative name for this mood workout",
      "mood": "{mood}",
      "why_this_workout": "Explanation of why this helps with {mood} mood",
      "duration": "{duration} minutes",
      "exercises": [
        {{"name": "", "sets_reps": "", "instructions": ""}}
      ],
      "mental_benefits": ["benefit1", "benefit2", ...],
      "motivation_tips": "Personal encouragement for someone feeling {mood}"
    }}"""

    try:
        response = model.generate_content(prompt)
        response_text = response.text
        
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0]
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0]
        
        workout = json.loads(response_text.strip())
        return jsonify(workout), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# ============= NEW FEATURE 4: POSE DETECTION - FORM CHECKING =============

@app.route("/check-exercise-form", methods=["POST"])
@login_required
def check_exercise_form():
    """Check exercise form from image"""
    data = request.json
    img_data = data.get("image")
    exercise_name = data.get("exercise", "squat")
    
    if not img_data:
        return jsonify({"error": "No image provided"}), 400
    
    try:
        # Decode base64 image
        img_bytes = base64.b64decode(img_data.split(',')[1])
        nparr = np.frombuffer(img_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            return jsonify({"error": "Invalid image"}), 400
        
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Analyze posture using existing function
        analysis = analyze_posture(image_rgb)
        
        # Get AI feedback on specific exercise form
        prompt = f"""The user is performing a {exercise_name.title()} exercise. 
        
Their posture analysis shows:
- Score: {analysis.get('score')}/100
- Overall: {analysis.get('overall')}
- Issues: {', '.join(analysis.get('issues', []))}
- Feedback: {', '.join(analysis.get('feedback', []))}

Based on this analysis, provide specific form corrections for {exercise_name}:
1. Main correction needed
2. Key points to fix
3. Safety tips
4. Performance improvement tips

Format as actionable advice with emojis."""

        response = model.generate_content(prompt)
        
        form_check = {
            "exercise": exercise_name,
            "posture_score": analysis.get('score'),
            "form_analysis": response.text,
            "timestamp": datetime.now().isoformat(),
            "raw_analysis": analysis
        }
        
        return jsonify(form_check), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ============= NEW FEATURE 5: ACHIEVEMENT SYSTEM =============

ACHIEVEMENT_BADGES = {
    "first_workout": {"name": "🏃 First Step", "description": "Complete your first workout", "points": 10},
    "week_streak": {"name": "🔥 Week Warrior", "description": "Workout 7 days in a row", "points": 50},
    "month_consistent": {"name": "⭐ Monthly Master", "description": "Workout 20+ days in a month", "points": 100},
    "50_workouts": {"name": "💪 50 Reps", "description": "Complete 50 workouts", "points": 150},
    "weight_loss": {"name": "📉 Transformation", "description": "Achieve 5kg weight loss", "points": 100},
    "strength_5x": {"name": "🦾 Strong as Hell", "description": "5x weight benchmark achieved", "points": 150},
    "calorie_tracker": {"name": "📊 Data Driven", "description": "Log 30 days of nutrition", "points": 75},
    "posture_perfect": {"name": "🧘 Perfect Posture", "description": "Achieve 90+ posture score", "points": 50},
    "mood_consistency": {"name": "😊 Mood Master", "description": "Complete 10 mood-based workouts", "points": 75},
    "transformation_complete": {"name": "🎯 Goal Crusher", "description": "Complete transformation plan", "points": 200}
}

@app.route("/unlock-achievement", methods=["POST"])
@login_required
def unlock_achievement():
    """Unlock an achievement for user"""
    username = session['user_id']
    data = request.json
    achievement_id = data.get("achievement_id")
    
    if achievement_id not in ACHIEVEMENT_BADGES:
        return jsonify({"error": "Achievement not found"}), 404
    
    achievements = load_achievements()
    if username not in achievements:
        achievements[username] = {"unlocked": [], "total_points": 0}
    
    # Check if already unlocked
    if achievement_id in achievements[username]["unlocked"]:
        return jsonify({"message": "Already unlocked", "already_had": True}), 200
    
    badge = ACHIEVEMENT_BADGES[achievement_id]
    achievements[username]["unlocked"].append(achievement_id)
    achievements[username]["total_points"] += badge["points"]
    achievements[username][f"{achievement_id}_unlocked_at"] = datetime.now().isoformat()
    
    save_achievements(achievements)
    
    return jsonify({
        "success": True,
        "achievement": achievement_id,
        "name": badge["name"],
        "description": badge["description"],
        "points": badge["points"],
        "total_points": achievements[username]["total_points"],
        "message": f"🎉 Achievement unlocked: {badge['name']}!"
    }), 200

@app.route("/get-achievements")
@login_required
def get_achievements():
    """Get user's achievements"""
    username = session['user_id']
    achievements = load_achievements()
    
    user_achievements = achievements.get(username, {"unlocked": [], "total_points": 0})
    
    # Build detailed achievement list
    achieved = []
    locked = []
    
    for achievement_id, badge_info in ACHIEVEMENT_BADGES.items():
        achievement_data = {
            "id": achievement_id,
            "name": badge_info["name"],
            "description": badge_info["description"],
            "points": badge_info["points"]
        }
        
        if achievement_id in user_achievements["unlocked"]:
            achievement_data["unlocked"] = True
            achievement_data["unlocked_at"] = user_achievements.get(f"{achievement_id}_unlocked_at")
            achieved.append(achievement_data)
        else:
            achievement_data["unlocked"] = False
            locked.append(achievement_data)
    
    return jsonify({
        "achieved": achieved,
        "locked": locked,
        "total_unlocked": len(achieved),
        "total_points": user_achievements.get("total_points", 0),
        "progress_percentage": (len(achieved) / len(ACHIEVEMENT_BADGES)) * 100
    }), 200

@app.route("/get-achievement-stats")
@login_required
def get_achievement_stats():
    """Get achievement statistics"""
    username = session['user_id']
    achievements = load_achievements()
    user_achievements = achievements.get(username, {"unlocked": [], "total_points": 0})
    
    stats = {
        "total_achievements": len(ACHIEVEMENT_BADGES),
        "unlocked_achievements": len(user_achievements["unlocked"]),
        "total_points": user_achievements.get("total_points", 0),
        "next_milestone": (len(user_achievements["unlocked"]) + 1) * 20,
        "progress_to_next": ((len(user_achievements["unlocked"]) % 1) * 100),
        "rank": get_achievement_rank(len(user_achievements["unlocked"]))
    }
    
    return jsonify(stats), 200

def get_achievement_rank(achievement_count):
    """Get user rank based on achievements"""
    if achievement_count == 0:
        return "Beginner 🌱"
    elif achievement_count < 3:
        return "Growing 📈"
    elif achievement_count < 5:
        return "Dedicated 💪"
    elif achievement_count < 7:
        return "Excellence 🌟"
    else:
        return "Legend 👑"

if __name__ == "__main__":
    app.run(debug=True)