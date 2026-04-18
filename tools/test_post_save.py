import json
import urllib.request

url = 'http://127.0.0.1:5000/api/save'
payload = {
    "results": {
        "body_analysis": {"age": 30, "height": 170, "weight": 70, "bmi": 24.22, "bmi_category":"Normal", "bmr":1600, "tdee":1900, "activity_level":"moderate"},
        "mental_health": {"sleep":7, "stress":3, "mood":7, "screen_time":3, "mental_score":6.5, "mental_status":"Moderate"},
        "fitness": {"sedentary_hours":5, "recovery_hours":8, "fitness_level":"Medium"},
        "wellness": {"wellness_score":72.5, "wellness_status":"Good"},
        "diet_recommendation": {"target_calories":1900, "goal":"maintain", "foods":[{"Food":"Apple","Calories":95,"Protein":0.5,"Carbs":25,"Fat":0.3}]}
    }
}

data = json.dumps(payload).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
with urllib.request.urlopen(req) as resp:
    print('Status:', resp.status)
    print(resp.read().decode('utf-8'))
