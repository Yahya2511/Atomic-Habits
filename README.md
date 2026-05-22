# Atomic-Habits
Trying to learn about FastAPI, so I am starting a project with a fun idea

I am following Corey Schafer's course:
[Python FastAPI Tutorial Series](https://youtube.com/playlist?list=PL-osiE80TeTsak-c-QsVeg0YYG_0TeyXI&si=5__lTOxhF8cOZ23X)

***

## What did I do till now?

* **Project Layout & Routing:** Set up the main structure of the project. Created routes to get all habits and to fetch a single habit by its ID.
* **API vs. UI Separation:** Configured the application so that API paths strictly start with `/api`. Used `include_in_schema=False` on the HTML routes so that the auto-generated Swagger documentation only displays the actual API endpoints.
* **Jinja2 Templating:** Implemented a base `layout.html` template using Jinja2 to help standardize and easily build out all other `.html` frontend pages.
* **Custom Error Handling:** Built custom exception handlers using `RequestValidationError` and the `starlette` library. The app now smartly returns a styled `error.html` page for UI requests, while maintaining strict JSON error responses for the `/api` routes.
* **Data Validation & Schemas (Pydantic):** Introduced Pydantic (`schemas.py`) to handle request and response validation. Created `HabitBase`, `HabitCreate`, and `HabitResponse` models to strictly define data types, enforce character limits, and control exactly what data goes in and out of the API.
* **POST Endpoints:** Created a `POST /api/habits` route utilizing the Pydantic schemas to safely create new habits, automatically assign incrementing IDs, and return the proper status codes (`201 CREATED`).