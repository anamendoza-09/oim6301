import bmi

result = bmi.calculate_bmi(weight=70, height=1.75)
print(f"The calculated BMI: {result:.2f}")

people = [
    {"name": "Alice", "weight": 68, "height": 1.65},
    {"name": "Bob", "weight": 85, "height": 1.80},
    {"name": "Charlie", "weight": 95, "height": 1.90},
    {"name": "Diana", "weight": 60, "height": 1.70},
    {"name": "Ethan", "weight": 78, "height": 1.75},
    {"name": "Fiona", "weight": 72, "height": 1.62},
]

for person in people:
    # print person
    weight = person["weight"]
    height = person["height"]
    bmi_value = bmi.compute_bmi(weight, height)
    category = bmi.classify_bmi(bmi_value)
    print(f"{person['name']}: has a BMI of {bmi_value:.2f}, which is classified as ({category})")