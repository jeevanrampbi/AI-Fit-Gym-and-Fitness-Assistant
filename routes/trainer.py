from fastapi import APIRouter, HTTPException
from models.schemas import PoseFrame, PoseFeedback
import random  # placeholder until real MediaPipe integration

# Module 1: AI Gym Trainer (Workout Detection & Feedback)
# Module 6: Pose-to-Performance Analyzer
# Real implementation would use MediaPipe or OpenPose for keypoint detection

router = APIRouter()

# simple rule-based feedback (will be replaced by actual CV model)
EXERCISE_TIPS = {
    "squat": {
        "common_errors": ["knee_cave", "forward_lean", "shallow_depth"],
        "tip": "Keep knees tracking over toes, chest up, go to parallel or below.",
    },
    "bench_press": {
        "common_errors": ["elbow_flare", "bar_path_inconsistent", "back_arch_too_much"],
        "tip": "Tuck elbows ~75°, bar to lower chest, keep feet flat.",
    },
    "pull_up": {
        "common_errors": ["kipping", "incomplete_rom", "shrug_at_top"],
        "tip": "Full dead hang to chin above bar. No kipping for strict form.",
    },
    "deadlift": {
        "common_errors": ["back_rounding", "bar_drift", "knees_shooting_forward"],
        "tip": "Neutral spine, bar close to body, push floor away.",
    },
}


@router.post("/analyze", response_model=PoseFeedback)
def analyze_pose(frame: PoseFrame):
    """
    Accepts pose keypoints and returns form feedback + performance score.
    In production: run keypoints through trained CNN/LSTM model.
    """
    exercise_info = EXERCISE_TIPS.get(frame.exercise.lower())
    if not exercise_info:
        raise HTTPException(status_code=400, detail=f"Exercise '{frame.exercise}' not supported yet")

    # placeholder scoring logic - real model would compute from keypoints
    form_score = round(random.uniform(60, 95), 1)
    detected_errors = random.sample(
        exercise_info["common_errors"],
        k=random.randint(0, min(2, len(exercise_info["common_errors"]))),
    )

    feedback_parts = []
    if detected_errors:
        feedback_parts.append(f"Issues detected: {', '.join(detected_errors).replace('_', ' ')}.")
    feedback_parts.append(exercise_info["tip"])

    performance_score = round((form_score * 0.6) + (random.uniform(70, 95) * 0.4), 1)

    return PoseFeedback(
        form_score=form_score,
        rep_count=frame.rep_number + 1,
        feedback=" ".join(feedback_parts),
        flags=detected_errors,
        performance_score=performance_score,
    )


@router.get("/exercises")
def list_supported_exercises():
    """Returns list of exercises the AI trainer currently supports."""
    return {"exercises": list(EXERCISE_TIPS.keys())}


@router.get("/weekly-report/{user_id}")
def weekly_report(user_id: str):
    """
    Returns a weekly performance summary for a user.
    TODO: pull from database once MongoDB is connected.
    """
    # hardcoded mock data for now
    return {
        "user_id": user_id,
        "week": "2025-W17",
        "avg_performance_score": 84.2,
        "total_sessions": 5,
        "most_improved": "bench_press",
        "needs_work": "pull_up",
        "streak_days": 7,
    }
