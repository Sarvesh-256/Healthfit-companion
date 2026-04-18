import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


def evaluate_mental_health(sleep_hours, stress_level, mood_level, screen_time):

    # Define fuzzy input variables
    sleep = ctrl.Antecedent(np.arange(0, 13, 1), 'sleep')
    stress = ctrl.Antecedent(np.arange(0, 11, 1), 'stress')
    mood = ctrl.Antecedent(np.arange(0, 11, 1), 'mood')
    screen = ctrl.Antecedent(np.arange(0, 13, 1), 'screen')

    # Output variable
    mental_health = ctrl.Consequent(np.arange(0, 11, 1), 'mental_health')

    # Membership functions
    sleep['low'] = fuzz.trimf(sleep.universe, [0, 0, 5])
    sleep['medium'] = fuzz.trimf(sleep.universe, [4, 7, 9])
    sleep['high'] = fuzz.trimf(sleep.universe, [8, 12, 12])

    stress['low'] = fuzz.trimf(stress.universe, [0, 0, 4])
    stress['medium'] = fuzz.trimf(stress.universe, [3, 5, 7])
    stress['high'] = fuzz.trimf(stress.universe, [6, 10, 10])

    mood['low'] = fuzz.trimf(mood.universe, [0, 0, 4])
    mood['medium'] = fuzz.trimf(mood.universe, [3, 5, 7])
    mood['high'] = fuzz.trimf(mood.universe, [6, 10, 10])

    screen['low'] = fuzz.trimf(screen.universe, [0, 0, 4])
    screen['medium'] = fuzz.trimf(screen.universe, [3, 6, 8])
    screen['high'] = fuzz.trimf(screen.universe, [7, 12, 12])

    mental_health['poor'] = fuzz.trimf(mental_health.universe, [0, 0, 4])
    mental_health['moderate'] = fuzz.trimf(mental_health.universe, [3, 5, 7])
    mental_health['good'] = fuzz.trimf(mental_health.universe, [6, 10, 10])

    # Rules (complete coverage)
    rule1 = ctrl.Rule(stress['high'] | sleep['low'] | screen['high'], mental_health['poor'])
    rule2 = ctrl.Rule(mood['low'], mental_health['poor'])
    rule3 = ctrl.Rule(stress['medium'] | sleep['medium'], mental_health['moderate'])
    rule4 = ctrl.Rule(mood['medium'], mental_health['moderate'])
    rule5 = ctrl.Rule(mood['high'] & stress['low'] & sleep['high'], mental_health['good'])
    rule6 = ctrl.Rule(mood['high'], mental_health['good'])

    # Control system
    mental_ctrl = ctrl.ControlSystem([
        rule1, rule2, rule3, rule4, rule5, rule6
    ])

    mental_sim = ctrl.ControlSystemSimulation(mental_ctrl)

    # Input values
    mental_sim.input['sleep'] = sleep_hours
    mental_sim.input['stress'] = stress_level
    mental_sim.input['mood'] = mood_level
    mental_sim.input['screen'] = screen_time

    # Compute
    mental_sim.compute()

    score = mental_sim.output['mental_health']

    # Convert score to label
    if score < 4:
        label = "Poor"
    elif score < 7:
        label = "Moderate"
    else:
        label = "Good"

    return round(score, 2), label