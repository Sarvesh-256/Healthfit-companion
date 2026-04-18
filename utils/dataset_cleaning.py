import pandas as pd

# File paths
food_path = "../data/food.csv"
nutrient_path = "../data/nutrient.csv"
food_nutrient_path = "../data/food_nutrient.csv"

# Load datasets
food = pd.read_csv(food_path)
nutrient = pd.read_csv(nutrient_path)
food_nutrient = pd.read_csv(food_nutrient_path)

print("Datasets loaded successfully")

# Nutrients we need
target_nutrients = [
    "Energy",
    "Protein",
    "Carbohydrate, by difference",
    "Total lipid (fat)"
]

# Filter required nutrients
nutrient_filtered = nutrient[nutrient["name"].isin(target_nutrients)]

# Merge with food_nutrient
merged = food_nutrient.merge(
    nutrient_filtered,
    left_on="nutrient_id",
    right_on="id"
)

# Merge with food table
merged = merged.merge(
    food,
    left_on="fdc_id",
    right_on="fdc_id"
)

# Keep important columns
merged = merged[["description", "name", "amount"]]

# Pivot table to get nutrients as columns
nutrition_table = merged.pivot_table(
    index="description",
    columns="name",
    values="amount"
).reset_index()

# Rename columns
nutrition_table = nutrition_table.rename(columns={
    "description": "Food",
    "Energy": "Calories",
    "Protein": "Protein",
    "Carbohydrate, by difference": "Carbs",
    "Total lipid (fat)": "Fat"
})

# Remove rows with missing values
nutrition_table = nutrition_table.dropna()

# Save cleaned dataset
output_path = "../data/nutrition_dataset.csv"
nutrition_table.to_csv(output_path, index=False)

print("Clean nutrition dataset created successfully!")
print("Saved at:", output_path)

print(nutrition_table.head())