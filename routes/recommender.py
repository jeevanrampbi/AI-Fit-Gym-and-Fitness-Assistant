from fastapi import APIRouter
from models.schemas import GymSearchRequest, GymResult
import math

# Module 7: Gym Recommender & Planner
# Recommends nearby gyms and workout programs based on user goal + location
# Real impl: use Google Places API + collaborative filtering model

router = APIRouter()

# mock gym database - replace with real DB query + Google Places API
MOCK_GYMS = [
    {
        "name": "Fitness One — Velachery",
        "lat": 12.9783, "lon": 80.2209,
        "price_per_month": 1200,
        "tags": ["barbells", "squat_rack", "cardio_zone"],
        "goals": ["muscle_gain", "strength"],
        "address": "100 Feet Rd, Velachery, Chennai",
    },
    {
        "name": "Gold's Gym — Adyar",
        "lat": 13.0012, "lon": 80.2565,
        "price_per_month": 2500,
        "tags": ["full_equipment", "pt_available", "pool", "sauna"],
        "goals": ["muscle_gain", "fat_loss", "maintenance"],
        "address": "Gandhi Nagar, Adyar, Chennai",
    },
    {
        "name": "Iron Paradise — T. Nagar",
        "lat": 13.0418, "lon": 80.2341,
        "price_per_month": 800,
        "tags": ["basic_equipment", "budget_friendly", "24hr"],
        "goals": ["maintenance", "fat_loss"],
        "address": "Pondy Bazaar, T. Nagar, Chennai",
    },
    {
        "name": "Anytime Fitness — OMR",
        "lat": 12.9010, "lon": 80.2279,
        "price_per_month": 2000,
        "tags": ["24hr", "modern_equipment", "ac", "app_access"],
        "goals": ["muscle_gain", "fat_loss", "maintenance"],
        "address": "Sholinganallur, OMR, Chennai",
    },
]

PROGRAM_RECOMMENDATIONS = {
    "muscle_gain": [
        {"name": "PPL (Push Pull Legs)", "days_per_week": 6, "level": "intermediate", "match": "best"},
        {"name": "PHUL (4-day strength/hypertrophy)", "days_per_week": 4, "level": "intermediate", "match": "great"},
        {"name": "Arnold Split", "days_per_week": 6, "level": "advanced", "match": "advanced"},
    ],
    "fat_loss": [
        {"name": "Full Body 3x/week + HIIT", "days_per_week": 5, "level": "beginner", "match": "best"},
        {"name": "PHUL with cardio", "days_per_week": 5, "level": "intermediate", "match": "great"},
        {"name": "CrossFit style", "days_per_week": 5, "level": "intermediate", "match": "good"},
    ],
    "maintenance": [
        {"name": "5x5 Stronglifts", "days_per_week": 3, "level": "beginner", "match": "best"},
        {"name": "Upper/Lower Split", "days_per_week": 4, "level": "intermediate", "match": "great"},
    ],
}


def haversine_distance(lat1, lon1, lat2, lon2) -> float:
    """Calculate distance between two coordinates in km."""
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return round(R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)), 2)


def score_gym(gym: dict, goal: str, budget: int | None) -> float:
    """Score a gym based on goal match and budget."""
    score = 0.5  # base score
    if goal in gym["goals"]:
        score += 0.3
    if budget and gym["price_per_month"] <= budget:
        score += 0.2
    return round(min(score, 1.0), 2)


@router.post("/search")
def search_gyms(req: GymSearchRequest):
    """Find and rank nearby gyms based on user goal + location."""
    results = []
    for gym in MOCK_GYMS:
        dist = haversine_distance(req.latitude, req.longitude, gym["lat"], gym["lon"])
        if dist > req.radius_km:
            continue

        match_score = score_gym(gym, req.goal, req.budget_inr)
        results.append(
            GymResult(
                name=gym["name"],
                distance_km=dist,
                price_per_month=gym["price_per_month"],
                match_score=match_score,
                tags=gym["tags"],
                address=gym["address"],
            )
        )

    results.sort(key=lambda x: x.match_score, reverse=True)
    return {"results": [r.dict() for r in results], "total_found": len(results)}


@router.get("/programs/{goal}")
def get_programs(goal: str):
    """Return recommended workout programs for a fitness goal."""
    programs = PROGRAM_RECOMMENDATIONS.get(goal)
    if not programs:
        return {"error": f"Unknown goal: {goal}. Use: muscle_gain, fat_loss, maintenance"}
    return {"goal": goal, "programs": programs}


@router.get("/challenges")
def get_active_challenges():
    """Return active fitness challenges users can join."""
    return {
        "challenges": [
            {"name": "30-Day Squat Challenge", "participants": 142, "days_left": 18, "difficulty": "medium"},
            {"name": "10k Steps Daily — April", "participants": 89, "days_left": 5, "difficulty": "easy"},
            {"name": "No Junk Food Week", "participants": 67, "days_left": 3, "difficulty": "hard"},
        ]
    }
