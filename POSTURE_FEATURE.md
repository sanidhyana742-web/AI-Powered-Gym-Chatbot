# 📷 Posture Detection Feature - Complete Guide

## Overview
The **Posture Checker** is an AI-powered real-time posture analysis feature that uses your device's camera and **MediaPipe Pose Detection** to analyze and improve your posture during workouts and daily activities.

## How It Works

### 1. **Technology Stack**
- **MediaPipe Pose**: Pre-trained deep learning model for detecting 33 body landmarks in real-time
- **OpenCV**: For image processing and manipulation
- **Web Camera API**: For accessing your device's camera
- **NumPy**: For mathematical calculations (angle calculations)

### 2. **What Gets Analyzed**

The posture checker analyzes 4 key areas:

#### **Shoulder Alignment**
- Detects if shoulders are level
- Issues: Uneven shoulders (can cause strain injuries)
- Target: < 5% difference in height

#### **Head Position**
- Detects forward head posture or backward tilt
- Issues: Forward head posture (text neck) causes neck strain
- Target: Head centered over shoulders

#### **Spine Alignment**
- Detects spine curve and alignment
- Issues: Curved spine, slouching
- Target: Straight vertical alignment

#### **Hip Alignment**
- Detects if hips are level
- Issues: Uneven weight distribution
- Target: Level hips

### 3. **Scoring System**

Your posture score is calculated as follows:

```
Base Score: 100

Penalties:
- Uneven shoulders: -15 points
- Forward head posture: -20 points
- Backward head tilt: -15 points
- Spine misalignment: -15 points
- Uneven hips: -10 points

Final Score: Base - All Penalties (minimum 0, maximum 100)
```

#### **Score Ranges**
- **85-100**: Excellent posture! ✅
- **70-84**: Good posture (minor adjustments needed)
- **50-69**: Fair posture (multiple adjustments recommended)
- **0-49**: Poor posture (significant adjustments needed)

## Getting Started

### **Step 1: Open Posture Checker**
- Navigate to the **Posture** page from any menu
- Or click: `Dashboard → 📷 Posture Checker`

### **Step 2: Grant Camera Permission**
- Click **"📷 Start Camera"**
- Allow browser to access your camera
- You should see your live video feed (horizontally flipped)

### **Step 3: Position Yourself**
```
✓ Full body visible in frame
✓ Standing upright and facing camera
✓ Good lighting from front
✓ Remove loose clothing for better detection
✓ Stand 6-8 feet away from camera
```

### **Step 4: Analyze Your Posture**
- Click **"✓ Analyze Posture"**
- Wait 2-3 seconds for analysis
- View your posture score and feedback

### **Step 5: Review Results**
Your analysis shows:
- **Score**: 0-100 rating
- **Status**: Excellent/Good/Fair/Poor
- **What's Good**: ✓ Correctly aligned body parts
- **Areas to Improve**: → Things to fix
- **Timestamp**: When the analysis was taken

## Tips for Best Results

### **Camera Setup**
1. Ensure adequate lighting (natural light ideal)
2. Clear background (less clutter = better detection)
3. Stand at arm's length distance (6-8 feet)
4. Keep entire body in view (head to feet)

### **Body Position**
1. Stand naturally, how you normally stand
2. Don't exaggerate posture (be realistic)
3. Wear fitted clothes if possible
4. Remove glasses/sunglasses if they obstruct face

### **Optimization Tips**
- Take multiple measurements for consistency
- Do it at the same time each day
- Track changes over time
- Use history to see improvement

## Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| "No person detected" | Not visible in camera | Make sure full body is in frame, move closer |
| Low accuracy | Poor lighting | Improve lighting from front |
| Inaccurate score | Partial body visible | Ensure head to feet are visible |
| Camera won't start | Permission denied | Allow camera access in browser settings |
| Wrong detection | Loose clothing | Wear fitted clothes |

## Posture Correction Exercises

### **For Forward Head Posture**
- Chin tucks (10 reps, 3 sets)
- Wall angels (10 reps, 3 sets)
- Neck stretches (hold 30 seconds)

### **For Uneven Shoulders**
- Heavy farmer carries (3 sets, 60 seconds)
- Single-armed rows (10 reps each side)
- Shoulder blade squeezes (15 reps, 3 sets)

### **For Spine Misalignment**
- Planks (hold 30-60 seconds, 3 sets)
- Dead bugs (10 reps, 3 sets)
- Bird dogs (10 reps each side, 3 sets)

### **For Uneven Hips**
- Glute bridges (15 reps, 3 sets)
- Single-leg glute bridges (12 reps each side)
- Fire hydrants (15 reps each side, 3 sets)

## Data Storage

### **What Gets Saved**
- Posture score
- Overall status
- Feedback given
- Issues identified
- Timestamp of analysis

### **Privacy**
- ✓ Your video feed is NOT saved
- ✓ Only analysis results stored
- ✓ Data stored locally in JSON file
- ✓ No third-party access to your video

### **History**
- Last 10 analyses kept
- View historical trends
- Clear history anytime
- Data persists across sessions

## API Endpoints

### **Analyze Posture**
```
POST /analyze-posture
Headers: Content-Type: application/json
Body: { "image": "data:image/jpeg;base64,..." }
Response: {
    "score": 75,
    "overall": "Good posture - minor adjustments needed",
    "feedback": ["✓ Shoulders perfectly aligned"],
    "issues": ["→ Head leaning forward - keep head neutral"],
    "timestamp": "2024-01-15T10:30:45.123456"
}
```

### **Get History**
```
GET /get-posture-history
Response: {
    "history": [
        { "score": 75, "overall": "Good posture...", ... },
        ...
    ]
}
```

### **Clear History**
```
POST /clear-posture-history
Response: { "success": true }
```

## Browser Compatibility

| Browser | Status | Notes |
|---------|--------|-------|
| Chrome | ✅ Full Support | Best performance |
| Edge | ✅ Full Support | Chromium-based |
| Firefox | ✅ Full Support | Works well |
| Safari | ⚠️ Limited | May require permissions |
| Mobile | ⚠️ Limited | Front camera works |

## Performance Notes

- **Analysis Time**: 1-3 seconds
- **Frame Rate**: Real-time (depends on device)
- **CPU Usage**: Moderate (may impact weak devices)
- **Internet**: Optional (runs locally)

## Troubleshooting

### **Q: Why can't I start my camera?**
A: Check browser permissions. Go to browser settings → Camera and allow access to the fitness chatbot.

### **Q: Why is my score inaccurate?**
A: Ensure:
1. Full body is visible
2. Good lighting
3. Standing naturally (not exaggerated)
4. Wearing fitted clothes

### **Q: Can I use this on my phone?**
A: Yes! Use your front-facing camera. Note: Smaller screen may make positioning harder.

### **Q: Is my video saved?**
A: No! Only your posture analysis scores are saved. Video is never stored.

### **Q: Can I use this for workout form feedback?**
A: Yes! Analyze your posture during exercises to ensure proper form and prevent injuries.

## Advanced Usage

### **Track Improvement**
1. Take a baseline posture analysis
2. Do posture correction exercises
3. Analyze again after 1 week
4. Compare scores in history

### **During Workouts**
1. Analyze posture before workout (baseline)
2. Do workout
3. Analyze posture after workout
4. Monitor fatigue impact on posture

### **Daily Check-in**
- Take 1-2 analyses per day
- Same time each day for consistency
- Watch score improve over time
- Share progress with trainer

## Integration with Other Features

The Posture Checker works alongside:
- **Workout Timer**: Analyze posture before/after HIIT workouts
- **Workout Generator**: Get form tips from AI coach
- **Chat**: Ask AI about posture correction exercises
- **Dashboard**: View posture analysis in activity history
- **Calculator**: Combine with body metrics

## Future Enhancements

Planned features:
- 🎥 Form correction videos
- 📊 Advanced analytics dashboard
- 🏆 Posture achievement badges
- 📢 Real-time alerts during workout
- 🤖 AI-powered form coaching
- 👥 Posture comparison with ideal forms
- 📈 Weekly/monthly posture reports

## Credits

- **MediaPipe**: Google's pre-trained pose detection model
- **OpenCV**: Computer vision library
- **Web APIs**: Browser camera and canvas APIs

---

## Summary

The Posture Checker is a powerful tool to:
✅ Monitor your posture in real-time
✅ Identify alignment issues
✅ Track improvement over time
✅ Prevent injury during exercise
✅ Build better posture habits

**Start using it today** → Navigate to `/posture` and analyze your posture!
