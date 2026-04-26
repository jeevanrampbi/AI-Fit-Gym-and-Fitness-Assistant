from fastapi import APIRouter
from models.schemas import ChatMessage, ChatResponse
import uuid
import os

# Module 5: Virtual Gym Buddy (AI Chat Companion)
# Uses sentiment analysis + conversational AI
# Connects to OpenAI/Hugging Face API for real responses
# For now: rule-based fallback responses

router = APIRouter()

# sentiment keywords - very basic, replace with proper NLP model
POSITIVE_KEYWORDS = ["great", "good", "motivated", "energized", "ready", "pumped", "awesome", "strong"]
NEGATIVE_KEYWORDS = ["tired", "lazy", "skip", "can't", "exhausted", "sick", "sore", "demotivated", "sad"]

RESPONSES = {
    "positive": [
        "That's the energy! Let's make today's session count 💪",
        "Love the attitude! Your body is ready — let's go.",
        "High energy detected! Time to crush those PRs.",
    ],
    "negative": [
        "Feeling low is normal. Even a 20-minute session beats zero. You've got this 🙌",
        "Recovery matters too. If you're genuinely sore, a light walk counts.",
        "Rough day? The gym might be exactly what you need to reset. Try showing up for just 10 mins.",
    ],
    "neutral": [
        "Ready when you are! What's on the plan today?",
        "Let's check your workout for today and take it one set at a time.",
        "How's the body feeling? We can adjust intensity based on how you're doing.",
    ],
}


def detect_sentiment(message: str) -> tuple[str, str]:
    """
    Very basic keyword-based sentiment detector.
    TODO: replace with Hugging Face sentiment model (cardiffnlp/twitter-roberta-base-sentiment).
    """
    msg_lower = message.lower()
    pos_score = sum(1 for w in POSITIVE_KEYWORDS if w in msg_lower)
    neg_score = sum(1 for w in NEGATIVE_KEYWORDS if w in msg_lower)

    if pos_score > neg_score:
        return "positive", "high"
    elif neg_score > pos_score:
        return "negative", "low"
    return "neutral", "medium"


def get_ai_response(message: str, sentiment: str) -> str:
    """
    Get response from AI model.
    TODO: call OpenAI / Hugging Face API here.
    Example:
        import openai
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are FitBuddy, a motivational AI gym companion..."},
                {"role": "user", "content": message}
            ]
        )
        return response.choices[0].message.content
    """
    import random
    responses = RESPONSES.get(sentiment, RESPONSES["neutral"])
    return random.choice(responses)


@router.post("/chat", response_model=ChatResponse)
def chat(msg: ChatMessage):
    """Send a message to the AI Gym Buddy and get a response."""
    session_id = msg.session_id or str(uuid.uuid4())
    sentiment, energy = detect_sentiment(msg.message)
    reply = get_ai_response(msg.message, sentiment)

    return ChatResponse(
        reply=reply,
        sentiment=sentiment,
        energy_level=energy,
        session_id=session_id,
    )


@router.get("/mood-history/{user_id}")
def mood_history(user_id: str):
    """
    Return mood/sentiment history for a user.
    TODO: store chat sessions in DB and query here.
    """
    return {
        "user_id": user_id,
        "last_7_days": [
            {"date": "2025-04-19", "sentiment": "positive", "energy": "high"},
            {"date": "2025-04-20", "sentiment": "neutral", "energy": "medium"},
            {"date": "2025-04-21", "sentiment": "negative", "energy": "low"},
            {"date": "2025-04-22", "sentiment": "positive", "energy": "high"},
            {"date": "2025-04-23", "sentiment": "positive", "energy": "high"},
            {"date": "2025-04-24", "sentiment": "neutral", "energy": "medium"},
            {"date": "2025-04-25", "sentiment": "positive", "energy": "high"},
        ],
    }
