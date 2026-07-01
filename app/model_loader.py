"""
Model Loader: Singleton pattern for loading ML artifacts once at startup.

Loads the trained model and scaler from disk exactly once.
Subsequent calls return the cached instances.
"""

import joblib
import os
from pathlib import Path

# Resolve model directory relative to this file's location
_BASE_DIR = Path(__file__).resolve().parent.parent
_MODEL_DIR = _BASE_DIR / "model"

# Module-level singletons: loaded once, reused forever
_model = None
_scaler = None
_feature_names = None


def _load_artifacts():
    """Load model, scaler, and feature names from disk. Called once."""
    global _model, _scaler, _feature_names

    model_path = _MODEL_DIR / "house_price_model.pkl"
    scaler_path = _MODEL_DIR / "scaler.pkl"
    feature_names_path = _MODEL_DIR / "feature_names.pkl"

    if not model_path.exists():
        raise FileNotFoundError(
            f"Model file not found at {model_path}. "
            "Run the training script first: python notebook/train_model.py"
        )
    if not scaler_path.exists():
        raise FileNotFoundError(
            f"Scaler file not found at {scaler_path}. "
            "Run the training script first: python notebook/train_model.py"
        )

    _model = joblib.load(model_path)
    _scaler = joblib.load(scaler_path)

    if feature_names_path.exists():
        _feature_names = joblib.load(feature_names_path)
    else:
        # Fallback to expected feature order
        _feature_names = [
            'Area Income', 'Area House Age', 'Area No of Rooms',
            'Area No of Bedrooms', 'Area Population'
        ]


def get_model():
    """Return the trained model. Loads from disk on first call."""
    if _model is None:
        _load_artifacts()
    return _model


def get_scaler():
    """Return the fitted scaler. Loads from disk on first call."""
    if _scaler is None:
        _load_artifacts()
    return _scaler


def get_feature_names():
    """Return the list of feature names in the expected order."""
    if _feature_names is None:
        _load_artifacts()
    return _feature_names


def load_all():
    """Explicitly load all artifacts. Call this at app startup."""
    _load_artifacts()
    return {
        "model": type(_model).__name__,
        "scaler": type(_scaler).__name__,
        "features": _feature_names,
    }
