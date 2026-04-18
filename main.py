from modules.bmi_tdee import calculate_bmi, bmi_category, calculate_bmr, calculate_tdee
from modules.fuzzy_mental_health import evaluate_mental_health
from modules.ann_fitness import predict_fitness
from modules.wellness_score import calculate_wellness_score
from modules.diet_recommendation import recommend_diet
from utils.data_storage import save_user_data
from utils.visualization import plot_weekly_progress

print("=== HealthFit Companion ===")

# -------------------------
# Basic User Inputs
# -------------------------

age = int(input("Enter age: "))
gender = input("Enter gender (male/female): ")

height = float(input("Enter height (cm): "))
weight = float(input("Enter weight (kg): "))

print("\nActivity Levels:")
print("1 - sedentary")
print("2 - light")
print("3 - moderate")
print("4 - active")
print("5 - very_active")

choice = int(input("Choose activity level (1-5): "))

activity_map = {
    1: "sedentary",
    2: "light",
    3: "moderate",
    4: "active",
    5: "very_active"
}

activity_level = activity_map.get(choice, "sedentary")

# -------------------------
# BMI + TDEE
# -------------------------

bmi = calculate_bmi(weight, height)
category = bmi_category(bmi)

bmr = calculate_bmr(weight, height, age, gender)
tdee = calculate_tdee(bmr, activity_level)

print("\n===== BODY ANALYSIS =====")
print("BMI:", bmi)
print("BMI Category:", category)
print("BMR:", bmr)
print("TDEE:", tdee)

# -------------------------
# STEP 3.2 GOES HERE
# Mental Health Inputs
# -------------------------

print("\n--- Mental Health Inputs ---")

sleep = float(input("Enter sleep hours per day: "))
stress = int(input("Enter stress level (0-10): "))
mood = int(input("Enter mood level (0-10): "))
screen = float(input("Enter screen time hours: "))

# -------------------------
# Fuzzy Evaluation
# -------------------------

mental_score, mental_status = evaluate_mental_health(
    sleep,
    stress,
    mood,
    screen
)

print("\n===== MENTAL HEALTH ANALYSIS =====")
print("Mental Health Score:", mental_score)
print("Mental Health Status:", mental_status)

# -------------------------
# STEP 4 GOES HERE
# Physical Activity Inputs
# -------------------------

print("\n--- Physical Activity Inputs ---")

activity = choice  # reuse earlier activity selection
sedentary = float(input("Sedentary hours per day: "))
recovery = float(input("Recovery/sleep hours: "))

# -------------------------
# STEP 5
# ANN Fitness Prediction
# -------------------------

fitness_level = predict_fitness(
    bmi,
    activity,
    sedentary,
    recovery
)

print("\n===== FITNESS ANALYSIS =====")
print("Fitness Level:", fitness_level)

wellness_score, wellness_status = calculate_wellness_score(
    bmi,
    mental_score,
    fitness_level
)

print("\n===== OVERALL WELLNESS =====")
print("Wellness Score:", wellness_score)
print("Health Status:", wellness_status)

print("\n===== DIET GOAL =====")
print("1 - Weight Loss")
print("2 - Maintain Weight")
print("3 - Weight Gain")

goal_choice = int(input("Choose your goal (1-3): "))

goal_map = {
    1: "loss",
    2: "maintain",
    3: "gain"
}

goal = goal_map.get(goal_choice, "maintain")

target_calories, foods = recommend_diet(tdee, goal)

print("\n===== DIET RECOMMENDATION =====")
print("Target Daily Calories:", target_calories)

print("\nSuggested Foods:")
print(foods[["Food", "Calories", "Protein", "Carbs", "Fat"]])

print("\n===== FINAL HEALTH SUMMARY =====")
print("BMI:", bmi, "| Category:", category)
print("Mental Health:", mental_status)
print("Fitness Level:", fitness_level)
print("Wellness Score:", wellness_score)
print("Recommended Daily Calories:", round(tdee))

print("\n--- Weekly Progress Inputs ---")
weekly_sleep = float(input("Enter average sleep hours per day for this week: "))
weekly_stress = int(input("Enter average stress level (0-10) for this week: "))
weekly_mood = int(input("Enter average mood level (0-10) for this week: "))
weekly_screen = float(input("Enter average screen time hours per day for this week: "))
weekly_sedentary = float(input("Enter average sedentary hours per day for this week: "))
weekly_recovery = float(input("Enter average recovery/sleep hours per day for this week: "))

save_user_data(
    age,
    bmi,
    mental_score,
    fitness_level,
    wellness_score,
    tdee,
    activity_level,
    weekly_sleep,
    weekly_stress,
    weekly_mood,
    weekly_screen,
    weekly_sedentary,
    weekly_recovery
)

view = input("\nDo you want to see your weekly progress graph? (yes/no): ")

if view.lower().startswith("y"):
    plot_weekly_progress()