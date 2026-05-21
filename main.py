from fastapi import FastAPI, Request, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

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

@app.get("/", include_in_schema=False, name="home")
@app.get("/habits", include_in_schema=False, name="habits")
def home(request: Request):
    return templates.TemplateResponse(
        request,
        "home.html",
        {"habits": habits}
    )

@app.get("/habits/{habit_id}", include_in_schema=False, name="habit_page")
def habit_page(request: Request, habit_id: int):
    for habit in habits:
        if habit.get("id") == habit_id:
            return templates.TemplateResponse(
                request,
                "habit.html",
                {"habit": habit}
            )
            
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Habit not found")

@app.get("/api/habits")
def get_habits():
    return habits

@app.get("/api/habits/{habit_id}")
def get_habit(habit_id: int):
    for habit in habits:
        if habit.get("id") == habit_id:
            return habit
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Habit not found")