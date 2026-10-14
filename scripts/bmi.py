bmi_value = 27

def classify_bmi(bmi):
    # print(bmi)
    if bmi >= 30:
        category ="Obese"
    elif bmi >= 25:
        category = "Overweight"
    elif bmi >= 18.5:
        category = "Normal"
    else:
        category = "Underweight"
    # print(category)
    return(category)

def compute_bmi(weight, height):
    bmi = weight / (height ** 2)
    return bmi


def calculate_bmi(weight, height):
    return compute_bmi(weight, height)


def main():
    weight_kg = float(input("Enter your weight in kg: "))
    height_m = float(input("Enter your height in meters: "))
    bmi_value = compute_bmi(weight_kg, height_m)
    result = classify_bmi(bmi_value)
    print(f"Your BMI is {bmi_value:.2f}, and your category is {result}.")


if __name__ == "__main__":
    main()
