# 👨‍💻 Developer Guide - FitnessAI

## For Developers & Customization

### Project Architecture

```
Frontend (HTML/CSS/JS)
        ↓
API Routes (Flask)
        ↓
AI Service (Google Gemini)
        ↓
Database (JSON → PostgreSQL)
```

### Code Organization

#### app.py Structure
```python
# 1. Imports & Configuration
# 2. Database Functions (load/save JSON)
# 3. Authentication Routes
# 4. User Profile Routes
# 5. Fitness Feature Routes
# 6. Chat & Memory Routes
# 7. Dashboard Routes
# 8. Page Routes
# 9. Main execution
```

#### Frontend Structure
```html
<!-- HTML: 6 main pages -->
1. home.html - Landing page
2. auth.html - Login/Register
3. chat.html - Main interface
4. dashboard.html - User stats
5. calculator.html - Tools
6. workout-timer.html - Timer

<!-- CSS: Complete styling -->
- Global styles
- Component styles
- Responsive design

<!-- JS: Feature logic -->
- Voice input
- Message sending
- Workout/meal generation
- History management
```

## 🔧 Customization Guide

### 1. Change Color Scheme

**Current Colors** (Edit style.css):
- Primary: `#FF6B6B` (Red)
- Secondary: `#FF8E72` (Orange)
- Dark: `#1a1a2e`

Replace all instances:
```css
/* Find & Replace in style.css */
#FF6B6B → your_color
#FF8E72 → your_secondary_color
#1a1a2e → your_dark_color
```

### 2. Modify AI Prompts

**Location**: app.py - `/chat` endpoint

**Current**:
```python
system_prompt = f"""You are a professional fitness coach..."""
```

**Customize**:
```python
system_prompt = f"""You are a [YOUR_SPECIALTY] coach..."""
```

### 3. Add New Features

**Example: Add Body Composition Analyzer**

1. Add route in app.py:
```python
@app.route("/analyze-body", methods=["POST"])
def analyze_body():
    data = request.json
    # Your logic here
    return jsonify({...})
```

2. Add button in chat.html:
```html
<button class="action-btn" onclick="analyzeBody()">Analyze Body</button>
```

3. Add function in script.js:
```javascript
async function analyzeBody() {
    let res = await fetch("/analyze-body", {
        method: "POST",
        body: JSON.stringify({...})
    });
    // Handle response
}
```

### 4. Upgrade Database

**Current**: JSON files
**Recommended**: PostgreSQL

1. Install psycopg2:
```bash
pip install psycopg2-binary SQLAlchemy flask-sqlalchemy
```

2. Update app.py imports:
```python
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:pass@localhost/fitnessai'
db = SQLAlchemy(app)
```

3. Define models:
```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120))
    password = db.Column(db.String(255))
    # ... other fields
```

4. Update database functions to use SQLAlchemy

### 5. Add Email Verification

1. Install:
```bash
pip install flask-mail
```

2. Configure in app.py:
```python
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
mail = Mail(app)
```

3. Send verification email in `/register` endpoint

### 6. Add Password Hashing

1. Install:
```bash
pip install werkzeug
```

2. In app.py:
```python
from werkzeug.security import generate_password_hash, check_password_hash

# When registering
users[username]["password"] = generate_password_hash(password)

# When logging in
if check_password_hash(stored_hash, provided_password):
    # Login successful
```

### 7. Deploy to Production

#### Option 1: Heroku

1. Create Procfile:
```
web: gunicorn app:app
```

2. Create runtime.txt:
```
python-3.9.7
```

3. Install gunicorn:
```bash
pip install gunicorn
```

4. Deploy:
```bash
heroku create your-app-name
git push heroku main
```

#### Option 2: AWS

1. Use Elastic Beanstalk
2. Configure environment variables
3. Set up RDS database
4. Configure S3 for static files

#### Option 3: DigitalOcean

1. Create Droplet
2. Install Python
3. Install dependencies
4. Use Nginx as reverse proxy
5. Use Systemd for service management

### 8. Add Analytics

```python
# In app.py
@app.before_request
def log_request():
    print(f"{request.path} - {request.method} - {datetime.now()}")

@app.after_request
def log_response(response):
    print(f"Response: {response.status_code}")
    return response
```

### 9. Add Testing

1. Install pytest:
```bash
pip install pytest
```

2. Create test_app.py:
```python
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
```

3. Run tests:
```bash
pytest test_app.py
```

### 10. Performance Optimization

#### Caching
```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/get-profile')
@cache.cached(timeout=300)
def get_profile():
    # Cached for 5 minutes
```

#### Compression
```python
from flask_compress import Compress
Compress(app)
```

#### Rate Limiting
```python
from flask_limiter import Limiter
limiter = Limiter(app)

@app.route('/chat', methods=['POST'])
@limiter.limit("30 per minute")
def chat():
    # Limited to 30 requests per minute
```

## 📚 File Reference

### Key Files to Modify

| File | Purpose | Difficulty |
|------|---------|-----------|
| app.py | Add routes, modify logic | Medium |
| templates/chat.html | Change UI layout | Easy |
| static/style.css | Change colors/design | Easy |
| static/script.js | Add functionality | Medium |

### Important Functions

**app.py**:
- `load_users()` / `save_users()` - Database operations
- `chat()` - Main AI interaction
- `generate_workout()` - Workout creation
- `calculate_calories()` - TDEE calculation

**script.js**:
- `sendMessage()` - Chat interaction
- `generateWorkout()` - Workout generation
- `calculateBMI()` / `calculateCalories()` - Calculations
- `toggleVoiceInput()` - Voice functionality

### Key Variables

```javascript
// Frontend configuration
const API_BASE_URL = '/'; // Change if API on different server
const TIMEOUT = 5000; // Request timeout

// Backend configuration
DEBUG = True # Set to False in production
MAX_CONTENT_LENGTH = 16 * 1024 * 1024 # Max upload size
```

## 🔍 Debugging

### Enable Debug Mode
```python
app.run(debug=True)
```

### Browser Console
Press `F12` to open developer tools
- JavaScript errors shown in Console
- Network requests in Network tab

### Server Logs
Look for errors in terminal running Flask

### Common Issues

1. **CORS Issues**: Add to app.py
```python
from flask_cors import CORS
CORS(app)
```

2. **Session Issues**: Check secret key setup
3. **API Errors**: Verify Gemini API key
4. **Database Errors**: Check file permissions

## 📊 Monitoring

### Track Usage
```python
# Add to database
interactions_log = []
interactions_log.append({
    'timestamp': datetime.now(),
    'endpoint': request.path,
    'user': session.get('user_id'),
    'status': response.status_code
})
```

### Performance Metrics
```python
import time

@app.before_request
def before_request():
    request.start_time = time.time()

@app.after_request
def after_request(response):
    duration = time.time() - request.start_time
    print(f"Request took {duration:.2f}s")
    return response
```

## 🚀 Advanced Features

### Add Machine Learning
```python
from sklearn.ensemble import RandomForestRegressor

# Train model on fitness data
# Use for advanced recommendations
```

### Add Real-time Features
```python
from flask_socketio import SocketIO, emit

socketio = SocketIO(app)

@socketio.on('message')
def handle_message(data):
    emit('response', {...})
```

### Add Payment Integration
```python
import stripe

stripe.api_key = "sk_test_..."

@app.route('/create-payment', methods=['POST'])
def create_payment():
    intent = stripe.PaymentIntent.create(...)
```

## 📖 Documentation

### Generate API Docs
```bash
pip install flask-swagger
```

### Code Comments Format
```python
"""
Function description.

Args:
    param1: Description
    param2: Description
Returns:
    dict: Description of return
"""
```

## 🤝 Contributing

1. Create feature branch
2. Make changes
3. Test locally
4. Submit pull request

## 📞 Support

For issues or questions:
1. Check existing code comments
2. Review Flask documentation
3. Check Gemini API docs
4. Search GitHub issues

---

**Happy Coding! 💻**
