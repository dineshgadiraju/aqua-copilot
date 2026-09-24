from sqlalchemy.orm import Session

from ..db_models import (
    PondDB,
    PondReadingDB,
    PondAlertDB,
)

from .forecast_service import (
    dissolved_oxygen_warning,
    ammonia_warning,
)


def get_pond_context(
    db: Session,
    pond_name: str,
):
    """
    Gather pond-specific information that can later
    be supplied to the AI Pond Assistant.
    """

    # ----------------------------
    # POND INFORMATION
    # ----------------------------

    pond = (
        db.query(PondDB)
        .filter(
            PondDB.pond_name == pond_name
        )
        .first()
    )

    if not pond:
        return {
            "status": "NOT_FOUND",
            "message": f"Pond '{pond_name}' was not found.",
        }

    # ----------------------------
    # RECENT READINGS
    # ----------------------------

    readings = (
        db.query(PondReadingDB)
        .filter(
            PondReadingDB.pond_name == pond_name
        )
        .order_by(
            PondReadingDB.recorded_at.desc()
        )
        .limit(10)
        .all()
    )

    # ----------------------------
    # FORECASTS
    # ----------------------------

    forecast_readings = sorted(
        readings,
        key=lambda reading: reading.recorded_at,
    )

    do_forecast = dissolved_oxygen_warning(
        forecast_readings,
        hours_ahead=6,
    )

    ammonia_forecast = ammonia_warning(
        forecast_readings,
        hours_ahead=6,
    )

    # ----------------------------
    # RECENT ALERTS
    # ----------------------------

    alerts = (
        db.query(PondAlertDB)
        .filter(
            PondAlertDB.pond_name == pond_name
        )
        .order_by(
            PondAlertDB.created_at.desc()
        )
        .limit(10)
        .all()
    )

    # ----------------------------
    # SERIALIZE READINGS
    # ----------------------------

    reading_data = []

    for reading in readings:
        reading_data.append(
            {
                "recorded_at": reading.recorded_at,
                "temperature_c": reading.temperature_c,
                "ph": reading.ph,
                "dissolved_oxygen_mg_l":
                    reading.dissolved_oxygen_mg_l,
                "salinity_ppt": reading.salinity_ppt,
                "ammonia_mg_l": reading.ammonia_mg_l,
                "feed_kg_day": reading.feed_kg_day,
                "shrimp_age_days": reading.shrimp_age_days,
                "stocking_density_per_m2":
                    reading.stocking_density_per_m2,
                "risk_level": reading.risk_level,
                "risk_probability":
                    reading.risk_probability,
            }
        )

    # ----------------------------
    # SERIALIZE ALERTS
    # ----------------------------

    alert_data = []

    for alert in alerts:
        alert_data.append(
            {
                "parameter": alert.parameter,
                "severity": alert.severity,
                "message": alert.message,
                "action": alert.action,
                "created_at": alert.created_at,
            }
        )

    # ----------------------------
    # COMPLETE CONTEXT
    # ----------------------------

    return {
        "status": "OK",

        "pond": {
            "pond_name": pond.pond_name,
            "location": pond.location,
            "area_m2": pond.area_m2,
            "species": pond.species,
        },

        "recent_readings": reading_data,

        "recent_alerts": alert_data,

        "forecasts": {
            "dissolved_oxygen": do_forecast,
            "ammonia": ammonia_forecast,
        },
    }