from pydantic import BaseModel
from typing import Optional, List


# ── Trainer / Pose ──────────────────────────────────────────────
class PoseFrame(BaseModel):
    # in real impl this would be base64 image or keypoints from MediaPipe
    keypoints: List[dict]
    exercise: str  # e.g. "squat", "bench_press", "pull_up"
    set_number: int
    rep_number: Optional[int] = 0


class PoseFeedback(BaseModel):
    form_score: float        # 0-100
    rep_count: int
    feedback: str
    flags: List[str]         # e.g. ["knee_cave", "back_rounding"]
    performance_score: float


# ── Diet ────────────────────────────────────────────────────────
class UserProfile(BaseModel):
    name: str
    age: int
    weight_kg: float
    height_cm: float
    goal: str               # "muscle_gain", "fat_loss", "maintenance"
    dietary_preference: str  # "veg", "non_veg", "vegan"
    activity_level: str     # "sedentary", "moderate", "active"


class MealPlan(BaseModel):
    total_calories: int
    protein_g: float
    carbs_g: float
    fats_g: float
    meals: List[dict]
    grocery_list: List[str]


class FoodLog(BaseModel):
    user_id: str
    food_name: str
    quantity_g: float
    meal_time: str  # "breakfast", "lunch", "dinner", "snack"


# ── Habits ──────────────────────────────────────────────────────
class WorkoutLog(BaseModel):
    user_id: str
    date: str           # "YYYY-MM-DD"
    completed: bool
    duration_mins: Optional[int] = None
    notes: Optional[str] = None


class SkipPrediction(BaseModel):
    date: str
    skip_probability: float   # 0.0 to 1.0
    risk_level: str           # "low", "medium", "high"
    nudge_message: str


# ── Buddy (Chat) ─────────────────────────────────────────────────
class ChatMessage(BaseModel):
    user_id: str
    message: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    reply: str
    sentiment: str       # "positive", "neutral", "negative"
    energy_level: str    # "high", "medium", "low"
    session_id: str


# ── IoT / Smart Gym ──────────────────────────────────────────────
class SensorData(BaseModel):
    device_id: str
    heart_rate: Optional[int] = None
    treadmill_speed: Optional[float] = None
    treadmill_incline: Optional[float] = None
    cable_resistance: Optional[float] = None
    calories_burned: Optional[float] = None
    session_duration_secs: Optional[int] = None


class IntensityRecommendation(BaseModel):
    recommended_zone: str       # "Zone 1" to "Zone 5"
    suggested_resistance: float
    next_rest_in_mins: float
    alert: Optional[str] = None


# ── Recommender ──────────────────────────────────────────────────
class GymSearchRequest(BaseModel):
    latitude: float
    longitude: float
    goal: str           # "muscle_gain", "fat_loss", "cardio"
    budget_inr: Optional[int] = None
    radius_km: Optional[float] = 5.0


class GymResult(BaseModel):
    name: str
    distance_km: float
    price_per_month: int
    match_score: float
    tags: List[str]
    address: str
