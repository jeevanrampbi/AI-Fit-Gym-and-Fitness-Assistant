# AI Gym & Fitness Assistant

> First Year Project — Computer Science Engineering -Artificial Intelligence and Machine Learning

An AI-powered gym and fitness management system that integrates workout detection, diet planning, behavioral tracking, IoT smart gym assistance, and conversational AI.

---

## Project Modules

| Module | Description | Status |
|--------|-------------|--------|
| AI Gym Trainer | Pose detection + rep counting using MediaPipe | Partial (mock) |
| Diet Coach | NLP-based meal plan + calorie tracker | Done (mock data) |
| Habit Tracker | Skip prediction + streak tracking | Done (mock model) |
| Gym Buddy | Conversational AI companion + sentiment analysis | Done (rule-based) |
| Smart Gym IoT | MQTT sensor integration + intensity recommendation | Done (mock) |
| Gym Recommender | Location-based gym + program recommender | Done (mock DB) |
| Pose Analyzer | Performance scoring from pose data | Partial |

---

## Tech Stack

- **Backend**: Python, FastAPI, Uvicorn
- **AI/ML**: MediaPipe, OpenCV, scikit-learn, Hugging Face Transformers
- **Database**: MongoDB (via PyMongo / Motor)
- **IoT**: MQTT (paho-mqtt), Node-RED
- **Frontend**: React.js / Next.js (separate repo)
- **Storage**: AWS S3 / Firebase
- **Analytics**: Plotly / D3.js

---

## Setup & Running

### 1. Clone the project
```bash
git clone https://github.com/your-username/aifit-backend
cd aifit-backend
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate      # on Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Create a `.env` file in the root:
```
MONGODB_URL=mongodb://localhost:27017
OPENAI_API_KEY=your_key_here        # optional, for buddy module
MQTT_BROKER=192.168.1.100
MQTT_PORT=1883
```

### 5. Run the server
```bash
uvicorn main:app --reload
```

Server runs at `http://localhost:8000`

---

## API Docs

Once the server is running, open:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## Project Structure

```
aifit/
├── main.py                  # FastAPI app entry point
├── requirements.txt
├── .env                     # environment variables (don't commit this!)
├── routes/
│   ├── trainer.py           # Module 1 + 6
│   ├── diet.py              # Module 2
│   ├── habits.py            # Module 4
│   ├── buddy.py             # Module 5
│   ├── iot.py               # Module 3
│   └── recommender.py       # Module 7
├── models/
│   └── schemas.py           # Pydantic request/response models
└── core/
    └── (config, db, etc.)   # coming in v0.2
```

---

## Known Limitations / TODO

- [ ] MongoDB integration not complete — using in-memory dicts for now
- [ ] MediaPipe pose detection is mocked — needs webcam/video pipeline
- [ ] Buddy chat uses rule-based responses — connect OpenAI API for real LLM
- [ ] Gym database is hardcoded — connect Google Places API for real results
- [ ] Skip prediction uses day-of-week heuristics — train proper ML model with real data
- [ ] No authentication yet — add JWT in v0.2

---

## Team

Built as part of the AI Gym & Fitness Assistant project for Unlox Academy, 2025.

---

## License

MIT — feel free to build on this.
