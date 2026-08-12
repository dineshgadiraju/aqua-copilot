from pathlib import Path
import json
import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import train_test_split

BASE = Path(__file__).parent
DATA_PATH = BASE / "data" / "shrimp_pond_data.csv"
MODEL_PATH = BASE / "models" / "pond_risk_model.joblib"
METRICS_PATH = BASE / "models" / "metrics.json"

FEATURES = [
    "temperature_c",
    "ph",
    "dissolved_oxygen_mg_l",
    "salinity_ppt",
    "ammonia_mg_l",
    "feed_kg_day",
    "shrimp_age_days",
    "stocking_density_per_m2",
]

df = pd.read_csv(DATA_PATH)
X = df[FEATURES]
y = df["high_risk"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

model = RandomForestClassifier(
    n_estimators=300,
    max_depth=10,
    min_samples_leaf=3,
    class_weight="balanced",
    random_state=42,
)

model.fit(X_train, y_train)

pred = model.predict(X_test)
proba = model.predict_proba(X_test)[:, 1]

report = classification_report(y_test, pred, output_dict=True)
auc = roc_auc_score(y_test, proba)

MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
joblib.dump({"model": model, "features": FEATURES}, MODEL_PATH)

metrics = {
    "roc_auc": round(float(auc), 4),
    "accuracy": round(float(report["accuracy"]), 4),
    "high_risk_precision": round(float(report["1"]["precision"]), 4),
    "high_risk_recall": round(float(report["1"]["recall"]), 4),
    "high_risk_f1": round(float(report["1"]["f1-score"]), 4),
}

METRICS_PATH.write_text(json.dumps(metrics, indent=2))

print("Model saved:", MODEL_PATH)
print(json.dumps(metrics, indent=2))
