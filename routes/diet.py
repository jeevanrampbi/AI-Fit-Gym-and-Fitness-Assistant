from fastapi import APIRouter, HTTPException
from models.schemas import UserProfile, MealPlan, FoodLog

# Module 2: AI Dietician & Calorie Coach
# Uses BMI + goal + dietary preference to generate meal plans
# NLP chatbot integration coming in v0.2

router = APIRouter()


def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    height_m = height_cm / 100
    return round(weight_kg / (height_m ** 2), 1)


def calculate_tdee(profile: UserProfile) -> int:
    """Harris-Benedict equation for TDEE calculation"""
    # BMR calculation (Mifflin-St Jeor)
    bmr = 10 * profile.weight_kg + 6.25 * profile.height_cm - 5 * profile.age
    # assuming male for now - TODO: add gender field in v0.2
    bmr += 5

    activity_multipliers = {
        "sedentary": 1.2,
        "moderate": 1.55,
        "active": 1.725,
    }
    multiplier = activity_multipliers.get(profile.activity_level, 1.55)
    return int(bmr * multiplier)


# meal templates - will be replaced with NLP-generated plans later
MEAL_TEMPLATES = {
    "muscle_gain": {
        "veg": [
            {"time": "breakfast", "items": ["Oats with milk", "Banana", "Peanut butter toast"], "calories": 520},
            {"time": "lunch", "items": ["Paneer rice bowl", "Dhal", "Salad"], "calories": 680},
            {"time": "dinner", "items": ["Roti + paneer curry", "Curd"], "calories": 570},
            {"time": "snack", "items": ["Protein shake", "Mixed nuts"], "calories": 330},
        ],
        "non_veg": [
            {"time": "breakfast", "items": ["Oats", "3 boiled eggs", "Banana"], "calories": 530},
            {"time": "lunch", "items": ["Chicken rice bowl", "Dhal", "Salad"], "calories": 680},
            {"time": "dinner", "items": ["Grilled chicken", "Sweet potato", "Broccoli"], "calories": 550},
            {"time": "snack", "items": ["Protein shake", "Mixed nuts"], "calories": 340},
        ],
    },
    "fat_loss": {
        "veg": [
            {"time": "breakfast", "items": ["Greek yogurt", "Berries", "Chia seeds"], "calories": 280},
            {"time": "lunch", "items": ["Quinoa salad", "Rajma", "Cucumber"], "calories": 450},
            {"time": "dinner", "items": ["Moong dal soup", "2 roti", "Sabzi"], "calories": 400},
            {"time": "snack", "items": ["Apple", "Handful of almonds"], "calories": 170},
        ],
        "non_veg": [
            {"time": "breakfast", "items": ["2 egg whites", "1 whole egg", "Oats"], "calories": 290},
            {"time": "lunch", "items": ["Grilled chicken salad", "Brown rice (small)"], "calories": 460},
            {"time": "dinner", "items": ["Baked fish", "Steamed veg", "Soup"], "calories": 380},
            {"time": "snack", "items": ["Protein shake (water)", "Apple"], "calories": 170},
        ],
    },
}

GROCERY_TEMPLATES = {
    "muscle_gain": ["Chicken breast 500g", "Eggs 12pk", "Oats 1kg", "Bananas", "Paneer 200g",
                    "Brown rice 1kg", "Peanut butter", "Protein powder", "Mixed nuts", "Curd 500ml"],
    "fat_loss": ["Chicken breast 500g", "Egg whites", "Greek yogurt", "Quinoa 500g",
                 "Rajma", "Broccoli", "Spinach", "Apples", "Almonds", "Cucumber"],
    "maintenance": ["Eggs 12pk", "Oats 1kg", "Brown rice 1kg", "Mixed vegetables",
                    "Chicken breast 300g", "Dhal", "Curd", "Fruits assorted", "Whole wheat roti"],
}


@router.post("/meal-plan", response_model=MealPlan)
def generate_meal_plan(profile: UserProfile):
    """Generate a personalized meal plan based on user profile."""
    bmi = calculate_bmi(profile.weight_kg, profile.height_cm)
    tdee = calculate_tdee(profile)

    # adjust calories by goal
    calorie_targets = {
        "muscle_gain": tdee + 300,
        "fat_loss": tdee - 400,
        "maintenance": tdee,
    }
    target_calories = calorie_targets.get(profile.goal, tdee)

    # pick template
    pref = profile.dietary_preference if profile.dietary_preference in ["veg", "non_veg"] else "non_veg"
    goal_key = profile.goal if profile.goal in MEAL_TEMPLATES else "muscle_gain"

    meals = MEAL_TEMPLATES.get(goal_key, {}).get(pref, MEAL_TEMPLATES["muscle_gain"]["non_veg"])
    grocery = GROCERY_TEMPLATES.get(goal_key, GROCERY_TEMPLATES["maintenance"])

    # rough macro split
    protein_g = round(profile.weight_kg * 2.0)  # 2g per kg for muscle gain
    fats_g = round(target_calories * 0.25 / 9)
    carbs_g = round((target_calories - (protein_g * 4) - (fats_g * 9)) / 4)

    return MealPlan(
        total_calories=target_calories,
        protein_g=protein_g,
        carbs_g=carbs_g,
        fats_g=fats_g,
        meals=meals,
        grocery_list=grocery,
    )


@router.post("/log-food")
def log_food(entry: FoodLog):
    """
    Log a food item for a user.
    TODO: store in MongoDB and accumulate daily totals.
    """
    # rough calorie lookup - in prod use a proper food database (USDA/Edamam API)
    rough_cals = round((entry.quantity_g / 100) * 150)  # ~150 kcal per 100g average placeholder
    return {
        "logged": True,
        "food": entry.food_name,
        "quantity_g": entry.quantity_g,
        "estimated_calories": rough_cals,
        "meal_time": entry.meal_time,
        "note": "Calorie estimate is approximate. Food DB integration coming in v0.2",
    }


@router.get("/bmi/{weight_kg}/{height_cm}")
def get_bmi(weight_kg: float, height_cm: float):
    """Quick BMI calculator endpoint"""
    bmi = calculate_bmi(weight_kg, height_cm)
    if bmi < 18.5:
        category = "underweight"
    elif bmi < 25:
        category = "healthy"
    elif bmi < 30:
        category = "overweight"
    else:
        category = "obese"
    return {"bmi": bmi, "category": category}
