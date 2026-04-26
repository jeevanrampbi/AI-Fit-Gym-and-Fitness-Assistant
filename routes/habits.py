from fastapi import APIRouter
from models.schemas import WorkoutLog, SkipPrediction
from datetime import datetime, timedelta
import random

# Module 4: AI Fitness Habit Tracker (Behavioral AI)
# Predicts skip probability using behavioral patterns
# Real impl: train a logistic regression / gradient boosting model on user history

router = APIRouter()

# in-memory store (replace with MongoDB in production)
workout_logs: dict = {}

MOTIVATIONAL_NUDGES = [
    "Hey, even 20 minutes is enough — don't break the streak! 🏃",
    "You've worked so hard this week. Don't let one day undo it 💪",
    "Your future self will thank you. Show up today.",
    "Rest days are planned. Unplanned skips hurt your progress.",
    "Remember why you started. One session at a time.",
    "Consistency > intensity. Just get to the gym.",
]


def predict_skip_probability(user_id: str, date: str) -> float:
    """
    Naive skip predictor based on day-of-week patterns.
    TODO: replace with trained ML model (scikit-learn / XGBoost).
    Features to add: sleep data, previous day intensity, mood logs, weather.
    """
    day = datetime.strptime(date, "%Y-%m-%d").weekday()
    # weekends and Wednesdays historically skipped more in our mock data
    base_probs = [0.12, 0.15, 0.41, 0.18, 0.22, 0.38, 0.67]
    base = base_probs[day]
    # add small noise to simulate model variance
    noise = random.uniform(-0.05, 0.05)
    return round(min(max(base + noise, 0.0), 1.0), 2)


@router.post("/log")
def log_workout(log: WorkoutLog):
    """Log whether a workout was completed or skipped."""
    key = f"{log.user_id}:{log.date}"
    workout_logs[key] = log.dict()
    return {"saved": True, "entry": log.dict()}


@router.get("/streak/{user_id}")
def get_streak(user_id: str):
    """
    Calculate current workout streak for a user.
    TODO: query from MongoDB in production.
    """
    # mock streak data for now
    return {
        "user_id": user_id,
        "current_streak": 7,
        "longest_streak": 14,
        "total_workouts_this_month": 18,
        "completion_rate_pct": 78,
    }


@router.get("/predict-skip/{user_id}")
def predict_next_7_days(user_id: str):
    """Predict skip risk for next 7 days."""
    today = datetime.now()
    predictions = []

    for i in range(1, 8):
        future_date = today + timedelta(days=i)
        date_str = future_date.strftime("%Y-%m-%d")
        prob = predict_skip_probability(user_id, date_str)

        if prob < 0.25:
            risk = "low"
        elif prob < 0.50:
            risk = "medium"
        else:
            risk = "high"

        nudge = random.choice(MOTIVATIONAL_NUDGES) if risk in ["medium", "high"] else ""

        predictions.append(
            SkipPrediction(
                date=date_str,
                skip_probability=prob,
                risk_level=risk,
                nudge_message=nudge,
            )
        )

    return {"user_id": user_id, "predictions": [p.dict() for p in predictions]}


@router.get("/calendar/{user_id}/{year}/{month}")
def get_calendar(user_id: str, year: int, month: int):
    """
    Return workout completion data for a given month.
    TODO: pull from DB. Returns mock data for now.
    """
    mock_data = {
        f"{year}-{str(month).zfill(2)}-{str(d).zfill(2)}": random.choice(["done", "done", "done", "skipped", "rest"])
        for d in range(1, 26)
    }
    return {"user_id": user_id, "year": year, "month": month, "days": mock_data}
