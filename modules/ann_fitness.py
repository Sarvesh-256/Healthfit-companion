import numpy as np
from sklearn.neural_network import MLPClassifier

# Training dataset (simple simulated data)
# [BMI, activity_level, sedentary_hours, recovery_hours]

X = np.array([
    [18, 3, 3, 8],
    [22, 4, 2, 7],
    [25, 3, 4, 7],
    [30, 2, 6, 6],
    [35, 1, 8, 5],
    [28, 2, 5, 6],
    [21, 4, 2, 8],
    [24, 3, 3, 7]
])

# Fitness labels
# 0 = Low
# 1 = Medium
# 2 = High

y = np.array([2, 2, 1, 1, 0, 1, 2, 1])

# Train ANN
model = MLPClassifier(hidden_layer_sizes=(5,), max_iter=2000)
model.fit(X, y)


def predict_fitness(bmi, activity, sedentary, recovery):

    input_data = np.array([[bmi, activity, sedentary, recovery]])

    prediction = model.predict(input_data)[0]

    labels = {
        0: "Low",
        1: "Medium",
        2: "High"
    }

    return labels[prediction]