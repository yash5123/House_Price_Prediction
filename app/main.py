from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import numpy as np

from app.schema import HouseFeatures, PredictionResponse, HealthResponse, ErrorResponse
from app.model_loader import get_model, get_scaler, get_feature_names, load_all


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load ML artifacts at startup
    info = load_all()
    print(f"Model loaded: {info['model']} | Scaler: {info['scaler']}")
    print(f"   Features: {info['features']}")
    yield
    print("Shutting down...")


# App initialization
app = FastAPI(
    title="House Price Prediction API",
    description="Predict US house prices based on area characteristics.",
    version="1.0.0",
    lifespan=lifespan,
    responses={
        422: {"model": ErrorResponse, "description": "Validation Error"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
    },
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend static files
frontend_dir = Path(__file__).resolve().parent.parent / "frontend"
if frontend_dir.exists():
    app.mount("/frontend", StaticFiles(directory=str(frontend_dir), html=True), name="frontend")


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": "Something went wrong while processing your request. Please check your input and try again.",
        },
    )


# Endpoints
@app.get("/", include_in_schema=False)
async def root():
    from fastapi.responses import RedirectResponse
    if frontend_dir.exists():
        return RedirectResponse(url="/frontend/index.html")
    return RedirectResponse(url="/docs")


@app.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    description="Simple health check endpoint.",
    tags=["System"],
)
async def health_check():
    model = get_model()
    return HealthResponse(
        status="healthy",
        model_loaded=model is not None,
        model_type=type(model).__name__,
    )


@app.post(
    "/predict",
    response_model=PredictionResponse,
    summary="Predict House Price",
    description="Predict house price based on area statistics.",
    tags=["Prediction"],
    responses={
        200: {
            "description": "Successful prediction",
            "content": {
                "application/json": {
                    "example": {
                        "predicted_price": 1232072.65,
                        "formatted_price": "$1,232,073",
                        "confidence": "High",
                    }
                }
            },
        }
    },
)
async def predict_price(features: HouseFeatures):
    try:
        model = get_model()
        scaler = get_scaler()
        
        # Build feature array in expected order
        feature_values = np.array([[
            features.area_income,
            features.area_house_age,
            features.area_no_of_rooms,
            features.area_no_of_bedrooms,
            features.area_population,
        ]])

        features_scaled = scaler.transform(feature_values)
        prediction = model.predict(features_scaled)[0]
        predicted_price = max(0, float(prediction))
        confidence = _assess_confidence(features)

        return PredictionResponse(
            predicted_price=round(predicted_price, 2),
            formatted_price=f"${predicted_price:,.0f}",
            confidence=confidence,
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )


def _assess_confidence(features: HouseFeatures) -> str:
    # Heuristics based on training data ranges
    typical_ranges = {
        "area_income": (17000, 110000),
        "area_house_age": (2.5, 10),
        "area_no_of_rooms": (3, 11),
        "area_no_of_bedrooms": (2, 7),
        "area_population": (100, 70000),
    }

    out_of_range_count = 0
    for field, (low, high) in typical_ranges.items():
        value = getattr(features, field)
        if value < low or value > high:
            out_of_range_count += 1

    if out_of_range_count == 0:
        return "High"
    elif out_of_range_count <= 2:
        return "Moderate"
    else:
        return "Low"
