from typing import Annotated
from datetime import datetime, timezone

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException as starletteHTTPException

import models
from database import Base, engine, get_db
from schemas import HabitCreate, HabitResponse, UserCreate, UserResponse

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
# Create a 'media' folder in your project root to avoid a crash here!
app.mount("/media", StaticFiles(directory="media"), name="media")

templates = Jinja2Templates(directory="templates")


# ==========================================
# HTML BROWSER ROUTES
# ==========================================

@app.get("/", include_in_schema=False, name="home")
@app.get("/habits", include_in_schema=False, name="habits")
def home(request: Request, db: Annotated[Session, Depends(get_db)]):
    # Fetch all habits from the database instead of dummy data
    result = db.execute(select(models.Habit))
    db_habits = result.scalars().all()
    
    return templates.TemplateResponse(
        request,
        "home.html",
        {"habits": db_habits}
    )

@app.get("/habits/{habit_id}", include_in_schema=False, name="habit_page")
def habit_page(request: Request, habit_id: int, db: Annotated[Session, Depends(get_db)]):
    # Fetch a single habit from the database
    result = db.execute(select(models.Habit).where(models.Habit.id == habit_id))
    db_habit = result.scalar_one_or_none()
    
    if db_habit:
        return templates.TemplateResponse(
            request,
            "habit.html",
            {"habit": db_habit}
        )

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Habit not found")


# ==========================================
# USER API ROUTES
# ==========================================

@app.post(
    "/api/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def create_user(user: UserCreate, db: Annotated[Session, Depends(get_db)]):
    # Check if username exists
    result = db.execute(select(models.User).where(models.User.user_name == user.user_name))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
        
    # Check if email exists
    result = db.execute(select(models.User).where(models.User.email == user.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
        
    # Create the user (TODO: Hash the password later!)
    new_user = models.User(
        user_name=user.user_name,
        email=user.email,
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/api/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalar_one_or_none()
    
    if user:
        return user
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


# ==========================================
# HABIT API ROUTES
# ==========================================

@app.get("/api/habits", response_model=list[HabitResponse])
def get_habits(db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Habit))
    return result.scalars().all()

@app.post(
    "/api/habits",
    response_model=HabitResponse, # We want to return the full Response with the ID
    status_code=status.HTTP_201_CREATED
)
def create_habit(habit: HabitCreate, db: Annotated[Session, Depends(get_db)]):
    # Since we don't have login yet, we will temporarily hardcode a creator_id
    # We will assume User ID 1 is creating this habit.
    
    new_habit = models.Habit(
        creator_id=1, # HARDCODED FOR NOW
        name=habit.name,
        description=habit.description,
        schedule_mask=habit.schedule_mask,
        start_date=habit.start_date,
        end_date=habit.end_date
    )
    
    db.add(new_habit)
    db.commit()
    db.refresh(new_habit)
    return new_habit

@app.get("/api/habits/{habit_id}", response_model=HabitResponse)
def get_habit(habit_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Habit).where(models.Habit.id == habit_id))
    db_habit = result.scalar_one_or_none()
    
    if db_habit:
        return db_habit
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Habit not found")


# ==========================================
# EXCEPTION HANDLERS
# ==========================================

@app.exception_handler(starletteHTTPException)
def general_http_exception_handler(request: Request, exception: starletteHTTPException):
    message = exception.detail if exception.detail else "An error occurred. Please check your request and try again."
    
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