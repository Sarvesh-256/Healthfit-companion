import pandas as pd

def recommend_diet(tdee, goal):

    # Adjust calories based on goal
    if goal == "loss":
        target_calories = tdee - 300
    elif goal == "gain":
        target_calories = tdee + 300
    else:
        target_calories = tdee

    # Load nutrition dataset
    df = pd.read_csv("data/nutrition_dataset.csv")

    # Sort foods by calories (ascending)
    df_sorted = df.sort_values(by="Calories")

    # Select some foods close to calorie target
    recommended_foods = df_sorted.sample(5)

    return round(target_calories), recommended_foods