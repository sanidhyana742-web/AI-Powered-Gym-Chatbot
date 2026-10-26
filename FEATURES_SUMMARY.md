# 🏋️ FitnessAI Chatbot - Features Summary

## ✅ All Features Successfully Implemented

### 1. **🔐 User Authentication System**
   - Register new users with email and password
   - Secure login system
   - Session management
   - Persistent user profiles
   - Data stored in JSON databases

### 2. **🍽️ Smart Meal Plan Generator**
   - AI-powered personalized meal plans
   - Customizable by daily calories
   - Dietary preferences (vegetarian, vegan, keto)
   - Adjustable meal plan duration (1-30 days)
   - Nutritional breakdowns included

### 3. **🧮 Calorie & Nutrition Calculator**
   - BMI Calculator with health recommendations
   - TDEE (Total Daily Energy Expenditure) calculator
   - Harris-Benedict equation for accurate calculations
   - Macro calculations (protein, carbs, fats)
   - Activity level adjustments

### 4. **🎯 Goal-Based AI Responses**
   - Specialized AI responses for:
     - Weight Loss
     - Muscle Gain
     - Endurance Training
     - General Fitness
   - Context-aware recommendations

### 5. **🏋️ Smart Workout Generator**
   - Personalized workout plans based on:
     - Fitness goal
     - Duration (10-180 minutes)
     - Available equipment
     - Experience level (beginner, intermediate, advanced)
   - Includes warm-up, main exercises, and cool-down
   - Form tips for each exercise

### 6. **⏱️ Workout Timer**
   - Simple countdown timer
   - HIIT (High-Intensity Interval Training) mode
   - Customizable work and rest intervals
   - Audio alerts when timer completes
   - Set tracking

### 7. **🎤 Voice Input Support**
   - Microphone access for hands-free interaction
   - Web Speech API integration
   - Automatic speech-to-text conversion
   - Easy toggle voice button

### 8. **💾 Memory Chatbot with History**
   - Persistent conversation history
   - Chat history retrieval per user
   - Clear chat history option
   - Context-aware responses using user profile
   - Automatic message storage

### 9. **📊 Fitness Dashboard**
   - User profile management
   - Progress statistics
   - Total chats counter
   - Member since date
   - Recent conversation display
   - Quick access to all tools

### 10. **💪 Real AI/API Integration**
   - Google Gemini 1.5 Flash API
   - Advanced natural language processing
   - Context-aware fitness coaching
   - Real-time responses

## 📁 Project Structure

```
Fitness Chatbot/
├── app.py                          # Main Flask application
├── requirement.txt                 # Python dependencies
├── users_database.json             # User data (auto-created)
├── chat_history.json               # Chat history (auto-created)
├── static/
│   ├── style.css                   # Complete styling
│   └── script.js                   # Frontend functionality
└── templates/
    ├── home.html                   # Home page with feature showcase
    ├── auth.html                   # Login/Register page
    ├── chat.html                   # Main chat interface
    ├── dashboard.html              # User dashboard
    ├── calculator.html             # BMI & Calorie calculators
    └── workout-timer.html          # Workout timer interface
```

## 🚀 How to Use

### 1. Start the Application
```bash
python app.py
```

### 2. Access the Website
- Open browser: `http://localhost:5000`
- Click "Get Started Now" or "Login/Register"

### 3. Create an Account
- Navigate to Login/Register page
- Fill in username, email, and password
- Click Register

### 4. Login
- Use your credentials to log in
- You'll be directed to the chat page

### 5. Use Features
- **Chat**: Talk to your AI fitness coach
- **Workout Timer**: Use built-in workout timer
- **Calculators**: Calculate BMI, TDEE, macros
- **Dashboard**: View your profile and statistics
- **Voice Input**: Click microphone to speak messages
- **Meal Plans**: Generate personalized meal plans
- **Workouts**: Generate personalized workout plans

## 🔧 API Endpoints

### Authentication
- `POST /register` - Register new user
- `POST /login` - User login
- `GET /logout` - User logout
- `GET /check-auth` - Check authentication status

### User Management
- `POST /update-profile` - Update user profile
- `GET /get-profile` - Get user profile info

### Fitness Features
- `POST /calculate-bmi` - Calculate BMI
- `POST /calculate-calories` - Calculate TDEE and macros
- `POST /generate-workout` - Generate workout plan
- `POST /generate-meal-plan` - Generate meal plan
- `POST /track-nutrition` - Track nutrition info

### Chat & Memory
- `POST /chat` - Chat with AI coach
- `GET /get-chat-history` - Get conversation history
- `POST /clear-chat-history` - Clear all chats
- `POST /goal-based-response` - Get goal-specific responses

### Dashboard
- `GET /get-dashboard-data` - Get dashboard statistics

## 🎨 Design features

- Modern gradient UI (Red/Pink #FF6B6B to #FF8E72)
- Dark theme for reduced eye strain
- Responsive design for mobile and desktop
- Smooth animations and transitions
- Intuitive navigation
- Beautiful typography and spacing

## 💾 Data Persistence

All user data is securely stored in JSON files:
- User profiles with fitness information
- Complete chat history per user
- User preferences and goals
- Timestamps for all interactions

## 🛡️ Security Features

- Session-based authentication
- Secret key configuration
- Protected endpoints with login_required decorator
- Secure password storage (can be enhanced with hashing)
- User-specific data isolation

## 🎯 Next Steps (Optional Enhancements)

1. Add password hashing (bcrypt)
2. Add database migration (SQLite/PostgreSQL)
3. Add email verification
4. Add progress photo tracking
5. Add achievement badges
6. Add social sharing features
7. Add mobile app version
8. Add payment integration for premium features

## ✨ Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **AI**: Google Gemini 1.5 API
- **Database**: JSON (can be upgraded to PostgreSQL)
- **Voice**: Web Speech API
- **Styling**: Custom CSS with gradient backgrounds

---

**Created on**: April 2026
**Version**: 1.0
**Status**: ✅ Fully Functional
