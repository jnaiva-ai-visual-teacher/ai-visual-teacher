import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai


# =========================================================
# ENVIRONMENT
# =========================================================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

gemini_client = None

if GEMINI_API_KEY:
    gemini_client = genai.Client(api_key=GEMINI_API_KEY)


# =========================================================
# FASTAPI APP
# =========================================================

app = FastAPI(
    title="JNAIVA AI Learning Platform",
    description="AI-powered visual learning platform",
    version="1.0.0"
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# BASIC ROUTES
# =========================================================

@app.get("/")
def root():
    return {
        "success": True,
        "message": "JNAIVA AI Learning API is running"
    }


@app.get("/api/health")
def health():
    return {
        "success": True,
        "status": "healthy",
        "gemini_configured": gemini_client is not None
    }


# =========================================================
# LEARNING TOPICS
# =========================================================

TOPICS = {

    "photosynthesis": {
        "id": "photosynthesis",
        "title": "Photosynthesis",
        "subject": "Biology",
        "description": "Learn how plants convert light energy into chemical energy.",
        "explanation": (
            "Photosynthesis is the process by which green plants "
            "use sunlight, carbon dioxide and water to produce glucose "
            "and oxygen."
        ),
        "key_points": [
            "Occurs mainly in the chloroplasts.",
            "Chlorophyll absorbs light energy.",
            "Carbon dioxide enters through stomata.",
            "Water is absorbed through the roots.",
            "Glucose is produced as food.",
            "Oxygen is released as a by-product."
        ],
        "formula": "6CO₂ + 6H₂O + light energy → C₆H₁₂O₆ + 6O₂"
    },

    "newtons-laws": {
        "id": "newtons-laws",
        "title": "Newton's Laws of Motion",
        "subject": "Physics",
        "description": "Understand the three fundamental laws describing motion.",
        "explanation": (
            "Newton's laws explain how forces affect the motion of objects. "
            "The three laws describe inertia, the relationship between force "
            "and acceleration, and action-reaction pairs."
        ),
        "key_points": [
            "First law: An object remains at rest or in uniform motion unless acted upon by an external force.",
            "Second law: Force equals mass multiplied by acceleration.",
            "Third law: Every action has an equal and opposite reaction."
        ],
        "formula": "F = ma"
    },

    "chemical-bonding": {
        "id": "chemical-bonding",
        "title": "Chemical Bonding",
        "subject": "Chemistry",
        "description": "Understand how atoms combine to form molecules and compounds.",
        "explanation": (
            "Chemical bonding is the attractive force that holds atoms "
            "together. Atoms form bonds to achieve greater stability."
        ),
        "key_points": [
            "Ionic bonds involve transfer of electrons.",
            "Covalent bonds involve sharing of electrons.",
            "Metallic bonds occur between metal atoms.",
            "Valence electrons play an important role in bonding."
        ],
        "formula": "Na⁺ + Cl⁻ → NaCl"
    },

    "python-basics": {
        "id": "python-basics",
        "title": "Python Basics",
        "subject": "Computer Science",
        "description": "Learn the fundamentals of Python programming.",
        "explanation": (
            "Python is a high-level programming language known for "
            "its simple syntax and wide range of applications."
        ),
        "key_points": [
            "Variables store values.",
            "Python uses indentation to define blocks.",
            "Functions are reusable blocks of code.",
            "Lists store multiple values.",
            "Conditional statements make decisions.",
            "Loops repeat instructions."
        ],
        "formula": None
    }
}


# =========================================================
# LEARNING ENDPOINTS
# =========================================================

@app.get("/api/learning/topics")
def get_topics():

    return {
        "success": True,
        "topics": list(TOPICS.values())
    }


@app.get("/api/learning/topic/{topic_id}")
def get_topic(topic_id: str):

    topic = TOPICS.get(topic_id)

    if not topic:
        return {
            "success": False,
            "error": "Topic not found"
        }

    return {
        "success": True,
        "topic": topic
    }


@app.get("/api/learning/search")
def search_topics(q: str = ""):

    query = q.strip().lower()

    if not query:
        return {
            "success": True,
            "results": []
        }

    results = []

    for topic in TOPICS.values():

        searchable_text = " ".join([
            topic["title"],
            topic["subject"],
            topic["description"],
            topic["explanation"]
        ]).lower()

        if query in searchable_text:
            results.append(topic)

    return {
        "success": True,
        "results": results
    }


# =========================================================
# QUIZZES
# =========================================================

QUIZZES = {

    "photosynthesis": [
        {
            "question": "Where does photosynthesis mainly occur?",
            "options": [
                "Mitochondria",
                "Chloroplasts",
                "Nucleus",
                "Ribosomes"
            ],
            "answer": 1,
            "explanation": "Photosynthesis mainly occurs in chloroplasts."
        },
        {
            "question": "Which gas is used by plants during photosynthesis?",
            "options": [
                "Oxygen",
                "Nitrogen",
                "Carbon dioxide",
                "Hydrogen"
            ],
            "answer": 2,
            "explanation": "Plants use carbon dioxide during photosynthesis."
        },
        {
            "question": "What is the main product of photosynthesis?",
            "options": [
                "Glucose",
                "Nitrogen",
                "Protein",
                "Salt"
            ],
            "answer": 0,
            "explanation": "Glucose is produced during photosynthesis."
        }
    ],

    "newtons-laws": [
        {
            "question": "Which formula represents Newton's second law?",
            "options": [
                "F = ma",
                "E = mc²",
                "V = IR",
                "P = VI"
            ],
            "answer": 0,
            "explanation": "Newton's second law is F = ma."
        }
    ],

    "chemical-bonding": [
        {
            "question": "What happens in an ionic bond?",
            "options": [
                "Electrons are transferred",
                "Neutrons are transferred",
                "Protons disappear",
                "Atoms disappear"
            ],
            "answer": 0,
            "explanation": "Ionic bonding involves transfer of electrons."
        }
    ],

    "python-basics": [
        {
            "question": "Which symbol is used to assign a value to a variable in Python?",
            "options": [
                "=",
                "==",
                "=>",
                ":="
            ],
            "answer": 0,
            "explanation": "The = operator assigns a value to a variable."
        }
    ]
}


@app.get("/api/quiz/{topic_id}")
def get_quiz(topic_id: str):

    quiz = QUIZZES.get(topic_id)

    if not quiz:
        return {
            "success": False,
            "error": "Quiz not found"
        }

    return {
        "success": True,
        "topic_id": topic_id,
        "questions": quiz
    }


# =========================================================
# PROGRESS
# =========================================================

progress = {
    "completed_topics": [],
    "quiz_scores": {},
    "streak": 0,
    "xp": 0
}


class ProgressRequest(BaseModel):
    topic_id: str


@app.get("/api/progress")
def get_progress():

    return {
        "success": True,
        "progress": progress
    }


@app.post("/api/progress")
def save_progress(data: ProgressRequest):

    topic_id = data.topic_id

    if topic_id not in progress["completed_topics"]:
        progress["completed_topics"].append(topic_id)
        progress["xp"] += 10

    return {
        "success": True,
        "progress": progress
    }


# =========================================================
# QUIZ SCORE
# =========================================================

class QuizScoreRequest(BaseModel):
    topic_id: str
    score: int
    total: int


@app.post("/api/quiz/score")
def save_quiz_score(data: QuizScoreRequest):

    progress["quiz_scores"][data.topic_id] = {
        "score": data.score,
        "total": data.total
    }

    progress["xp"] += data.score * 5

    return {
        "success": True,
        "progress": progress
    }


# =========================================================
# JNAIVA AI
# =========================================================

class AIAskRequest(BaseModel):
    message: str
    topic: str | None = None


@app.post("/api/ai/ask")
def ask_ai(data: AIAskRequest):

    # Check Gemini configuration
    if not gemini_client:

        return {
            "success": False,
            "error": "Gemini API key is not configured."
        }

    topic = data.topic or "General"

    # Prompt for JNAIVA
    prompt = f"""
You are JNAIVA, an AI learning companion.

Topic:
{topic}

Student question:
{data.message}

Teach the student clearly and accurately.

Rules:
- Explain in simple language.
- Break difficult concepts into small steps.
- Give an example when useful.
- Use formulas when relevant.
- Do not unnecessarily make the answer very long.
- If the student seems confused, explain it more simply.
- Never pretend to know something you are unsure about.
- Focus on helping the student understand rather than simply giving an answer.
"""

    try:

        chat = gemini_client.chats.create(
            model="gemini-3.5-flash-lite"
        )

        response = chat.send_message(prompt)

        return {
            "success": True,
            "answer": response.text
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }


# =========================================================
# STARTUP MESSAGE
# =========================================================

@app.on_event("startup")
def startup_event():

    print("=" * 50)
    print("JNAIVA AI Learning API")
    print("=" * 50)
    print("Server started successfully.")

    if gemini_client:
        print("Gemini AI: CONFIGURED")
    else:
        print("Gemini AI: NOT CONFIGURED")

    print("=" * 50)
