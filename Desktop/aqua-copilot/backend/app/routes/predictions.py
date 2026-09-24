from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..db_models import PondReadingDB, PondAlertDB
from ..schemas import PondReading
from ..services.forecast_service import (
    dissolved_oxygen_warning,
    ammonia_warning,
)
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
        risk_level, probability = predict_pond_risk(reading)

    except FileNotFoundError as e:
        return {
            "error": str(e)
        }

    # Generate explanation and recommendations
    factors, actions = explain(reading)

    # Generate parameter-specific alerts
    alerts = generate_alerts(reading)

    # Save pond reading
    db_reading = PondReadingDB(
        pond_name=reading.pond_name,
        temperature_c=reading.temperature_c,
        ph=reading.ph,
        dissolved_oxygen_mg_l=reading.dissolved_oxygen_mg_l,
        salinity_ppt=reading.salinity_ppt,
        ammonia_mg_l=reading.ammonia_mg_l,
        feed_kg_day=reading.feed_kg_day,
        shrimp_age_days=reading.shrimp_age_days,
        stocking_density_per_m2=reading.stocking_density_per_m2,
        risk_level=risk_level,
        risk_probability=probability
    )

    db.add(db_reading)
    db.commit()
    db.refresh(db_reading)

    # Save every generated alert
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

    # Commit alerts after the loop
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

@router.get("/ponds/{pond_name}/forecast")
def forecast_pond(
    pond_name: str,
    hours: int = 6,
    db: Session = Depends(get_db),
):
    # Prevent unrealistic forecast windows
    hours = max(1, min(hours, 24))

    readings = (
        db.query(PondReadingDB)
        .filter(
            PondReadingDB.pond_name == pond_name
        )
        .order_by(
            PondReadingDB.recorded_at.asc()
        )
        .all()
    )

    if not readings:
        return {
            "status": "NO_DATA",
            "message": f"No readings found for pond '{pond_name}'.",
        }

    return dissolved_oxygen_warning(
        readings,
        hours_ahead=hours,
    )

@router.get("/ponds/{pond_name}/forecast/ammonia")
def forecast_ammonia(
    pond_name: str,
    hours: int = 6,
    db: Session = Depends(get_db),
):
    # Limit forecast window to 1–24 hours
    hours = max(1, min(hours, 24))

    readings = (
        db.query(PondReadingDB)
        .filter(
            PondReadingDB.pond_name == pond_name
        )
        .order_by(
            PondReadingDB.recorded_at.asc()
        )
        .all()
    )

    if not readings:
        return {
            "status": "NO_DATA",
            "message": f"No readings found for pond '{pond_name}'.",
        }

    return ammonia_warning(
        readings,
        hours_ahead=hours,
    )