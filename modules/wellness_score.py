def calculate_wellness_score(bmi, mental_score, fitness_level):

    # BMI scoring
    if bmi < 18.5:
        bmi_score = 60
    elif bmi < 25:
        bmi_score = 90
    elif bmi < 30:
        bmi_score = 70
    else:
        bmi_score = 50

    # Fitness level scoring
    fitness_scores = {
        "Low": 40,
        "Medium": 70,
        "High": 90
    }

    fitness_score = fitness_scores.get(fitness_level, 50)

    # Mental health already 0–10 scale
    mental_scaled = mental_score * 10

    # Weighted combination
    wellness_score = (
        0.3 * bmi_score +
        0.4 * mental_scaled +
        0.3 * fitness_score
    )

    # Classification
    if wellness_score < 40:
        status = "Poor"
    elif wellness_score < 60:
        status = "Average"
    elif wellness_score < 80:
        status = "Good"
    else:
        status = "Excellent"

    return round(wellness_score, 2), status