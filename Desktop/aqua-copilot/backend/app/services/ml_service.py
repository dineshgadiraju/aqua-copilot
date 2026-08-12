from pathlib import Path

import joblib
import pandas as pd


MODEL_PATH = (
    Path(__file__).resolve().parents[3]
    / "ml"
    / "models"
    / "pond_risk_model.joblib"
)


def predict_pond_risk(reading):

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "Model not found. "
            "Run the ML training pipeline first."
        )

    bundle = joblib.load(MODEL_PATH)

    model = bundle["model"]
    features = bundle["features"]

    model_input = reading.model_dump()

    model_input.pop("pond_name")

    row = pd.DataFrame(
        [model_input]
    )[features]

    probability = float(
        model.predict_proba(row)[0, 1]
    )

    if probability >= 0.70:
        risk_level = "HIGH"

    elif probability >= 0.35:
        risk_level = "MEDIUM"

    else:
        risk_level = "LOW"

    return risk_level, probability