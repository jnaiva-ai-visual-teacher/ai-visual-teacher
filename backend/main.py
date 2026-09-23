from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


app = FastAPI(
    title="AI Visual Teacher API",
    description="Backend API for AI Visual Teacher",
    version="1.0.0"
)


# Allow the frontend to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LearningRequest(BaseModel):
    topic: str


@app.get("/")
def home():
    return {
        "message": "AI Visual Teacher API is running 🚀"
    }


@app.get("/api/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/api/explain")
def explain(request: LearningRequest):

    topic = request.topic.strip()

    if not topic:
        return {
            "success": False,
            "message": "Please provide a topic."
        }

    return {
        "success": True,
        "topic": topic,
        "title": f"Understanding {topic}",
        "explanation": (
            f"This is a demo explanation for {topic}. "
            "The real AI explanation system will be connected next."
        ),
        "simple_explanation": (
            f"Let's understand {topic} step by step "
            "using simple language and visual examples."
        ),
        "key_points": [
            f"Understand the basic concept of {topic}.",
            "Break the concept into smaller parts.",
            "Use examples and visualizations.",
            "Test your understanding with a quiz."
        ]
    }


@app.post("/api/quiz")
def quiz(request: LearningRequest):

    topic = request.topic.strip()

    return {
        "success": True,
        "topic": topic,
        "question": f"What is an important first step when learning {topic}?",
        "options": [
            "Understand the basic concept",
            "Memorize everything immediately",
            "Skip the fundamentals",
            "Avoid examples"
        ],
        "answer": 0
    }
