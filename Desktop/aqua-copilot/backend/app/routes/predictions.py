from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..db_models import PondReadingDB, PondAlertDB
from ..schemas import PondReading

from ..services.ml_service import predict_pond_risk
from ..services.alert_service import generate_alerts
from ..services.recommendation_service import explain


router = APIRouter(
    tags=["Predictions"]
)


@router.post("/predict-risk")
def predict_risk(
    reading: PondReading,
    db: Session = Depends(get_db)
):

    try:
        risk_level, probability = (
            predict_pond_risk(reading)
        )

    except FileNotFoundError as e:
        return {
            "error": str(e)
        }

    factors, actions = explain(reading)

    alerts = generate_alerts(reading)

    db_reading = PondReadingDB(
        pond_name=reading.pond_name,
        temperature_c=reading.temperature_c,
        ph=reading.ph,
        dissolved_oxygen_mg_l=(
            reading.dissolved_oxygen_mg_l
        ),
        salinity_ppt=reading.salinity_ppt,
        ammonia_mg_l=reading.ammonia_mg_l,
        feed_kg_day=reading.feed_kg_day,
        shrimp_age_days=reading.shrimp_age_days,
        stocking_density_per_m2=(
            reading.stocking_density_per_m2
        ),
        risk_level=risk_level,
        risk_probability=probability
    )

    db.add(db_reading)
    db.commit()
    db.refresh(db_reading)

    for alert in alerts:

        db_alert = PondAlertDB(
        reading_id=db_reading.id,
        pond_name=reading.pond_name,
        parameter=alert["parameter"],
        severity=alert["severity"],
        message=alert["message"],
        action=alert["action"]
    )

    db.add(db_alert)

    db.commit()

    return {
        "reading_id": db_reading.id,
        "pond_name": reading.pond_name,
        "risk_level": risk_level,
        "risk_probability": round(
            probability,
            3
        ),
        "main_factors": factors,
        "recommended_actions": actions,
        "alerts": alerts
    }


@router.get("/readings")
def get_readings(
    db: Session = Depends(get_db)
):
    readings = (
        db.query(PondReadingDB)
        .order_by(
            PondReadingDB.recorded_at.desc()
        )
        .all()
    )

    return readings