import joblib
from pathlib import Path

_BASE_DIR = Path(__file__).resolve().parent.parent
_MODEL_DIR = _BASE_DIR / "model"

_model = None
_scaler = None
_feature_names = None


def _load_artifacts():
    global _model, _scaler, _feature_names

    model_path = _MODEL_DIR / "house_price_model.pkl"
    scaler_path = _MODEL_DIR / "scaler.pkl"
    feature_names_path = _MODEL_DIR / "feature_names.pkl"

    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found at {model_path}.")
    if not scaler_path.exists():
        raise FileNotFoundError(f"Scaler file not found at {scaler_path}.")

    _model = joblib.load(model_path)
    _scaler = joblib.load(scaler_path)

    if feature_names_path.exists():
        _feature_names = joblib.load(feature_names_path)
    else:
        _feature_names = [
            'Area Income', 'Area House Age', 'Area No of Rooms',
            'Area No of Bedrooms', 'Area Population'
        ]


def get_model():
    if _model is None:
        _load_artifacts()
    return _model


def get_scaler():
    if _scaler is None:
        _load_artifacts()
    return _scaler


def get_feature_names():
    if _feature_names is None:
        _load_artifacts()
    return _feature_names


def load_all():
    _load_artifacts()
    return {
        "model": type(_model).__name__,
        "scaler": type(_scaler).__name__,
        "features": _feature_names,
    }
