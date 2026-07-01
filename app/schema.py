from pydantic import BaseModel, Field


class HouseFeatures(BaseModel):
    area_income: float = Field(
        ...,
        ge=0,
        le=500000,
        description="Average income of residents in the area ($)",
        json_schema_extra={"example": 68000.0}
    )
    area_house_age: float = Field(
        ...,
        ge=0,
        le=100,
        description="Average age of houses in the area (years)",
        json_schema_extra={"example": 6.0}
    )
    area_no_of_rooms: float = Field(
        ...,
        ge=1,
        le=30,
        description="Average number of rooms per house in the area",
        json_schema_extra={"example": 7.0}
    )
    area_no_of_bedrooms: float = Field(
        ...,
        ge=0,
        le=20,
        description="Average number of bedrooms per house in the area",
        json_schema_extra={"example": 4.0}
    )
    area_population: float = Field(
        ...,
        ge=0,
        le=200000,
        description="Population of the area",
        json_schema_extra={"example": 36000.0}
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "area_income": 68583.11,
                    "area_house_age": 5.98,
                    "area_no_of_rooms": 6.99,
                    "area_no_of_bedrooms": 3.98,
                    "area_population": 36163.52,
                }
            ]
        }
    }


class PredictionResponse(BaseModel):
    predicted_price: float = Field(
        ...,
        description="Predicted house price in USD"
    )
    formatted_price: str = Field(
        ...,
        description="Human-readable formatted price string"
    )
    confidence: str = Field(
        ...,
        description="Rough confidence indicator based on input feature ranges"
    )


class HealthResponse(BaseModel):
    status: str = Field(default="healthy")
    model_loaded: bool = Field(default=True)
    model_type: str = Field(default="LinearRegression")


class ErrorResponse(BaseModel):
    error: str = Field(..., description="Error type or message")
    detail: str = Field(..., description="Detailed error description")
