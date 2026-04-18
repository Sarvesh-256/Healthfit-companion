def calculate_bmi(weight, height):
    """
    weight in kg
    height in cm
    """
    height_m = height / 100
    bmi = weight / (height_m ** 2)
    return round(bmi, 2)


def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"


def calculate_bmr(weight, height, age, gender):
    """
    Mifflin-St Jeor Equation
    """
    if gender.lower() == "male":
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161

    return round(bmr, 2)


def calculate_tdee(bmr, activity_level):
    """
    activity_level options:
    sedentary
    light
    moderate
    active
    very_active
    """

    activity_multipliers = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725,
        "very_active": 1.9
    }

    multiplier = activity_multipliers.get(activity_level, 1.2)

    tdee = bmr * multiplier

    return round(tdee, 2)