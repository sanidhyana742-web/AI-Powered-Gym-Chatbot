# 🚀 FitnessAI Setup & Installation Guide

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Gemini API Key (free tier available at https://ai.google.dev)

## Installation Steps

### Step 1: Install Dependencies

```bash
pip install -r requirement.txt
```

This will install:
- Flask 2.3.0
- google-generativeai 0.5.0
- python-dotenv 1.0.0
- Werkzeug 2.3.0

### Step 2: Configure API Key

The Gemini API key is already set in `app.py`. If you need to update it:

1. Go to https://ai.google.dev
2. Get your API key
3. Update the line in `app.py`:
   ```python
   genai.configure(api_key="YOUR_API_KEY_HERE")
   ```

### Step 3: Run the Application

```bash
python app.py
```

The application will start at `http://localhost:5000`

## First Time Usage

### 1. Access the Home Page
- Open browser to `http://localhost:5000`
- See feature overview and benefits

### 2. Create Account
- Click "Get Started Now" button
- Click "Register here" on the login page
- Fill in:
  - Username
  - Email
  - Password
  - Confirm Password

### 3. Login
- Use your credentials to log in
- Redirected to chat interface

### 4. Set Up Profile
- Enter your age
- Select your fitness goal
- Update full profile in Dashboard

## Feature Usage Guide

### 💬 Chat with AI Coach
1. Type your fitness question
2. Click "Send" or press Enter
3. AI provides personalized response
4. Or click 🎤 to use voice input

### 🏋️ Generate Workout
1. Click "🏋️ Workout" button in sidebar
2. Select duration, equipment, and level
3. Click "Generate Workout"
4. AI creates personalized plan

### 🍽️ Generate Meal Plan
1. Click "🍽️ Meal Plan" button in sidebar
2. Set daily calories, dietary preference, days
3. Click "Generate Meal Plan"
4. Get full meal with calories

### 🧮 Calculate Metrics
1. Go to "🧮 Calculators" page
2. For BMI: Enter weight and height
3. For Calories: Enter age, weight, height, gender, activity level
4. Get results with recommendations

### ⏱️ Workout Timer
1. Go to "⏱️ Workout Timer" page
2. Choose Simple Timer or HIIT mode
3. Set duration and sets
4. Click Start
5. Get audio alert when complete

### 📊 View Dashboard
1. Click "Dashboard" in navbar
2. See your statistics
3. Update profile information
4. View recent conversations

## Troubleshooting

### Issue: "ModuleNotFoundError"
**Solution**: Reinstall requirements
```bash
pip install -r requirement.txt
```

### Issue: API Key Error
**Solution**: Verify the API key is correct and has permission
- Check at https://console.cloud.google.com
- Ensure Gemini API is enabled

### Issue: Port Already in Use
**Solution**: Change port in app.py or kill process:
```bash
python app.py --port 5001
```

### Issue: Database Errors
**Solution**: Delete existing database files and restart
```bash
rm users_database.json chat_history.json
python app.py
```

### Issue: Voice Input Not Working
**Solution**: 
- Allow microphone access
- Use HTTPS (Chrome requires it for microphone)
- Try different browser

## File Descriptions

| File | Purpose |
|------|---------|
| `app.py` | Main Flask application with all routes |
| `requirement.txt` | Python package dependencies |
| `static/style.css` | Complete CSS styling |
| `static/script.js` | Frontend JavaScript logic |
| `templates/home.html` | Landing page |
| `templates/auth.html` | Login/Register page |
| `templates/chat.html` | Chat interface |
| `templates/dashboard.html` | User dashboard |
| `templates/calculator.html` | Calculator tools |
| `templates/workout-timer.html` | Timer interface |
| `users_database.json` | User profiles (auto-created) |
| `chat_history.json` | Conversation history (auto-created) |

## Security Notes

1. **Change Secret Key**: In production, update `app.secret_key` in app.py
2. **Use HTTPS**: Deploy with SSL/TLS certificate
3. **Hash Passwords**: Upgrade from plain text to bcrypt
4. **Database**: Use PostgreSQL instead of JSON for production
5. **Environment Variables**: Move API key to .env file

## Performance Tips

1. Database backups: Regularly backup JSON files
2. Cache responses: Add caching for repeated requests
3. Limit history: Archive old chat history
4. API optimization: Use streaming for long responses

## Browser Compatibility

- ✅ Chrome/Chromium 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+
- ⚠️ Older browsers may have limited functionality

## Mobile Access

- Responsive design works on tablets and phones
- Works best on 768px+ width screens
- Touch-friendly buttons and input fields
- Voice input works on mobile with microphone

## Getting Help

1. Check browser console for errors (F12)
2. Verify all packages installed: `pip list`
3. Check Gemini API status at https://status.cloud.google.com
4. Review application logs in terminal

## Next Steps After Setup

1. Explore all features in the demo
2. Create multiple test accounts
3. Generate different workout and meal plans
4. Test voice input and chat history
5. Check dashboard statistics
6. Read FEATURES_SUMMARY.md for complete feature list

---

**Last Updated**: April 2026
**Version**: 1.0.0
