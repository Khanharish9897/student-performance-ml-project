from pathlib import Path

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.pipeline.predict_pipeline import CustomData, PredictPipeline


# ---------------------------------------------------------
# FastAPI application
# ---------------------------------------------------------

app = FastAPI(
    title="Student Performance Predictor",
    description="Predict a student's math score",
    version="1.0.0",
)

# Optional alias used by some deployment platforms
application = app


# ---------------------------------------------------------
# Project folders
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

templates = Jinja2Templates(
    directory=str(TEMPLATES_DIR)
)

# Mount static folder only if it exists
if STATIC_DIR.exists():
    app.mount(
        "/static",
        StaticFiles(directory=str(STATIC_DIR)),
        name="static",
    )


# ---------------------------------------------------------
# Home page: show HTML form
# ---------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def show_home_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={
            "result": None,
            "error": None,
            "form_data": {},
        },
    )


# ---------------------------------------------------------
# Handle HTML form submission
# ---------------------------------------------------------

@app.post("/predict", response_class=HTMLResponse)
async def predict_math_score(
    request: Request,

    gender: str = Form(...),

    race_ethnicity: str = Form(...),

    parental_level_of_education: str = Form(...),

    lunch: str = Form(...),

    test_preparation_course: str = Form(...),

    reading_score: float = Form(
        ...,
        ge=0,
        le=100,
    ),

    writing_score: float = Form(
        ...,
        ge=0,
        le=100,
    ),
):
    form_data = {
        "gender": gender,
        "race_ethnicity": race_ethnicity,
        "parental_level_of_education": (
            parental_level_of_education
        ),
        "lunch": lunch,
        "test_preparation_course": (
            test_preparation_course
        ),
        "reading_score": reading_score,
        "writing_score": writing_score,
    }

    try:
        # Create student data object
        student_data = CustomData(
            gender=gender,
            race_ethnicity=race_ethnicity,
            parental_level_of_education=(
                parental_level_of_education
            ),
            lunch=lunch,
            test_preparation_course=(
                test_preparation_course
            ),
            reading_score=reading_score,
            writing_score=writing_score,
        )

        # Convert submitted values into a DataFrame
        prediction_dataframe = (
            student_data.get_data_as_data_frame()
        )

        print("Prediction input:")
        print(prediction_dataframe)

        # Run prediction pipeline
        prediction_pipeline = PredictPipeline()

        prediction = prediction_pipeline.predict(
            prediction_dataframe
        )

        predicted_math_score = round(
            float(prediction[0]),
            2,
        )

        # Return the same page with prediction result
        return templates.TemplateResponse(
            request=request,
            name="home.html",
            context={
                "result": predicted_math_score,
                "error": None,
                "form_data": form_data,
            },
        )

    except Exception as error:
        return templates.TemplateResponse(
            request=request,
            name="home.html",
            context={
                "result": None,
                "error": str(error),
                "form_data": form_data,
            },
            status_code=500,
        )


# ---------------------------------------------------------
# Health-check route
# ---------------------------------------------------------

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "message": "Student performance API is running",
    }

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )