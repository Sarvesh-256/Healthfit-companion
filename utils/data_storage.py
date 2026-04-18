import pandas as pd
from datetime import datetime, timedelta
import os

def save_user_data(age, bmi, mental_score, fitness_level, wellness_score, tdee,
                   activity_level, weekly_sleep, weekly_stress,
                   weekly_mood, weekly_screen, weekly_sedentary,
                   weekly_recovery):

    file_path = "data/health_history.csv"

    week_start = (datetime.now() - timedelta(days=datetime.now().weekday())).strftime("%Y-%m-%d")

    new_data = {
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "WeekStart": week_start,
        "Age": age,
        "BMI": bmi,
        "MentalScore": mental_score,
        "FitnessLevel": fitness_level,
        "WellnessScore": wellness_score,
        "TDEE": tdee,
        "ActivityLevel": activity_level,
        "WeeklySleep": weekly_sleep,
        "WeeklyStress": weekly_stress,
        "WeeklyMood": weekly_mood,
        "WeeklyScreenTime": weekly_screen,
        "WeeklySedentary": weekly_sedentary,
        "WeeklyRecovery": weekly_recovery
    }

    df_new = pd.DataFrame([new_data])

    if os.path.exists(file_path):
        df_old = pd.read_csv(file_path)
        df = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df = df_new

    df.to_csv(file_path, index=False)

    print("\n✅ Data saved successfully!")