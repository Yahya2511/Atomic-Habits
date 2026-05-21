from fastapi import FastAPI, Request, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as starletteHTTPException

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

@app.exception_handler(starletteHTTPException)
def general_http_exception_handler(request: Request, exception: starletteHTTPException):
    message = (
        exception.detail
        if exception.detail
        else "An error occurred. Please check your request and try again."
    )
    
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": message}
        )
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": exception.status_code,
            "title": exception.status_code,
            "message": message
        },
        status_code=exception.status_code
    )
    
@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exception: RequestValidationError):
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"detail": exception.errors()}
        )
    
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "title": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "message": "Invalid request. Please check your input and try again."
        },
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT
    )