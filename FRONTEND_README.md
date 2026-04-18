# HealthFit Companion - Frontend Setup Guide

## Overview

A modern web-based frontend has been added to the HealthFit Companion project! The frontend provides an intuitive interface for users to input their health data and receive comprehensive assessments.

## What's New

### New Files Added:
```
app.py                           # Flask backend server
templates/
  └── index.html                 # Main web interface
static/
  ├── css/
  │   └── style.css             # Complete styling
  └── js/
      └── script.js             # Frontend logic
```

### Features:

✅ **User-Friendly Interface**
- Clean, modern dashboard design
- Responsive layout (works on desktop, tablet, mobile)
- Real-time form validation

✅ **Health Assessment Form**
- Basic Information (Age, Gender, Height, Weight, Activity Level)
- Mental Health Metrics (Sleep, Stress, Mood, Screen Time)
- Physical Activity Data (Sedentary Hours, Recovery Hours)

✅ **Comprehensive Results Display**
- Body Analysis (BMI, BMR, TDEE)
- Mental Health Score & Status
- Fitness Level Assessment
- Overall Wellness Score
- Personalized Diet Recommendations

✅ **Additional Features**
- Save assessments to database
- Download results as CSV report
- Real-time slider feedback
- Loading animations
- Error handling
- Mobile-responsive design

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Flask Server

```bash
python app.py
```

The server will start on: **http://localhost:5000**

### 3. Open in Browser

Navigate to `http://localhost:5000` in your web browser

## How to Use

1. **Fill out the Assessment Form**
   - Enter your personal information
   - Select your activity level
   - Provide mental health metrics
   - Input physical activity data

2. **Generate Assessment**
   - Click "Generate Assessment" button
   - Wait for calculations to complete

3. **View Results**
   - See comprehensive health analysis
   - Get personalized diet recommendations
   - View wellness scores and metrics

4. **Save or Export**
   - Save your assessment for future reference
   - Download as CSV report for keeping records

## Technology Stack

- **Backend:** Flask (Python)
- **Frontend:** HTML5, CSS3, JavaScript (ES6)
- **Design:** Responsive, Mobile-First
- **Data:** Real-time calculations using existing modules

## Project Structure

```
HeathFit companion/
├── app.py                    # Flask app (NEW)
├── main.py                   # Original CLI interface
├── requirements.txt          # Python dependencies (UPDATED)
├── data/                     # Health data files
├── modules/
│   ├── ann_fitness.py
│   ├── bmi_tdee.py
│   ├── diet_recommendation.py
│   ├── fuzzy_mental_health.py
│   └── wellness_score.py
├── utils/
│   ├── data_storage.py
│   ├── dataset_cleaning.py
│   └── visualization.py
├── templates/                # HTML templates (NEW)
│   └── index.html
└── static/                   # CSS & JavaScript (NEW)
    ├── css/
    │   └── style.css
    └── js/
        └── script.js
```

## Features Breakdown

### Body Analysis
- BMI Calculation and Category
- Basal Metabolic Rate (BMR)
- Total Daily Energy Expenditure (TDEE)

### Mental Health
- Mental Health Score
- Status Assessment
- Sleep hour tracking
- Stress level evaluation
- Screen time monitoring

### Fitness
- Fitness level prediction
- Sedentary hours tracking
- Recovery hours analysis

### Wellness Score
- Overall wellness rating (0-100)
- Visual progress indicator
- Comprehensive health summary

### Diet Recommendation
- Personalized nutrition guidance
- Based on BMI category and TDEE
- Tailored to individual metrics

## Deployment

For production deployment, consider:

1. **Remove Debug Mode**
   ```python
   app.run(debug=False, port=5000)
   ```

2. **Use Production Server**
   ```bash
   pip install gunicorn
   gunicorn app:app
   ```

3. **Set Environment Variables**
   ```bash
   export FLASK_ENV=production
   ```

## Troubleshooting

**Port 5000 already in use:**
```bash
python app.py --port 5001
# or modify in app.py: app.run(port=5001)
```

**Module import errors:**
- Ensure all dependencies in your original modules are installed
- Make sure you're running from the project root directory

**Frontend not loading styles:**
- Clear browser cache (Ctrl+Shift+Delete)
- Ensure Flask is serving static files correctly

## Support

For issues or questions about the frontend integration, ensure:
- All backend modules are properly implemented
- Flask and dependencies are correctly installed
- You're running the app from the project root directory
- JavaScript is enabled in your browser

Enjoy using HealthFit Companion! 🏥💪🧠
