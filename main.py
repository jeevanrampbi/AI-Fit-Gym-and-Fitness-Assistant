from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import trainer, diet, habits, buddy, iot, recommender

# NOTE: this is the main entry point for the AI Gym & Fitness Assistant API
# run with: uvicorn main:app --reload

app = FastAPI(
    title="AI Gym & Fitness Assistant API",
    description="Backend for the AI-powered gym and fitness assistant system",
    version="0.1.0",
)

# allow frontend to call the API (adjust origins in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# register all module routes
app.include_router(trainer.router, prefix="/trainer", tags=["AI Trainer"])
app.include_router(diet.router, prefix="/diet", tags=["Diet Coach"])
app.include_router(habits.router, prefix="/habits", tags=["Habit Tracker"])
app.include_router(buddy.router, prefix="/buddy", tags=["Gym Buddy"])
app.include_router(iot.router, prefix="/iot", tags=["Smart Gym IoT"])
app.include_router(recommender.router, prefix="/recommender", tags=["Gym Recommender"])


@app.get("/")
def root():
    return {"message": "AI Gym & Fitness Assistant API is running", "version": "0.1.0"}


@app.get("/health")
def health():
    return {"status": "ok"}
