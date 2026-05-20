from fastapi import FastAPI
from fastapi.responses import HTMLResponse


app = FastAPI()

# --- DUMMY DATA ---

habits = [
    {
        "id": 1,
        "name": "Study",
        "description": "You need to become better",
        "frequency_type": "daily",
        "goal_value": 4,
        "created_at": "2026-05-18T08:00:00"
    },
    {
        "id": 2,
        "name": "Read",
        "description": "Read any book",
        "frequency_type": "daily",
        "goal_value": 30,
        "created_at": "2026-05-19T09:30:00"
    }
]

habit_logs = [
    {
        "id": 1,
        "habit_id": 1,
        "logged_date": "2026-05-20",
        "is_completed": True
    },
    {
        "id": 2,
        "habit_id": 2,
        "logged_date": "2026-05-20",
        "is_completed": False
    }
]

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
@app.get("/habits", response_class=HTMLResponse, include_in_schema=False)
def home():
    return f"<h1>{habits[0]['name']}</h1>"

@app.get("/api/habits")
def get_habits():
    return habits