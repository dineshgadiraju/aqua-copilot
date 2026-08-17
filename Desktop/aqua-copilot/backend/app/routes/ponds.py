from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..db_models import (
    PondDB,
    PondReadingDB,
    PondAlertDB
)
from ..schemas import PondCreate
from ..services.trend_service import analyze_pond_trends


router = APIRouter(
    prefix="/ponds",
    tags=["Ponds"]
)


@router.post("")
def create_pond(
    pond: PondCreate,
    db: Session = Depends(get_db)
):
    existing_pond = (
        db.query(PondDB)
        .filter(
            PondDB.pond_name == pond.pond_name
        )
        .first()
    )

    if existing_pond:
        return {
            "error":
            f"Pond '{pond.pond_name}' already exists."
        }

    db_pond = PondDB(
        pond_name=pond.pond_name,
        location=pond.location,
        area_m2=pond.area_m2,
        species=pond.species
    )

    db.add(db_pond)
    db.commit()
    db.refresh(db_pond)

    return db_pond


@router.get("")
def get_ponds(
    db: Session = Depends(get_db)
):
    ponds = (
        db.query(PondDB)
        .order_by(
            PondDB.created_at.desc()
        )
        .all()
    )

    return ponds


@router.get("/{pond_id}")
def get_pond(
    pond_id: int,
    db: Session = Depends(get_db)
):
    pond = (
        db.query(PondDB)
        .filter(PondDB.id == pond_id)
        .first()
    )

    if not pond:
        return {
            "error": "Pond not found."
        }

    return pond


@router.get("/{pond_id}/readings")
def get_pond_readings(
    pond_id: int,
    db: Session = Depends(get_db)
):
    pond = (
        db.query(PondDB)
        .filter(PondDB.id == pond_id)
        .first()
    )

    if not pond:
        return {
            "error": "Pond not found."
        }

    readings = (
        db.query(PondReadingDB)
        .filter(
            PondReadingDB.pond_name
            == pond.pond_name
        )
        .order_by(
            PondReadingDB.recorded_at.desc()
        )
        .all()
    )

    return {
        "pond": {
            "id": pond.id,
            "pond_name": pond.pond_name,
            "location": pond.location,
            "area_m2": pond.area_m2,
            "species": pond.species
        },
        "total_readings": len(readings),
        "readings": readings
    }
@router.get("/{pond_id}/alerts")
def get_pond_alerts(
    pond_id: int,
    db: Session = Depends(get_db)
):

    pond = (
        db.query(PondDB)
        .filter(PondDB.id == pond_id)
        .first()
    )

    if not pond:
        return {
            "error": "Pond not found."
        }

    alerts = (
        db.query(PondAlertDB)
        .filter(
            PondAlertDB.pond_name
            == pond.pond_name
        )
        .order_by(
            PondAlertDB.created_at.desc()
        )
        .all()
    )

    return {
        "pond_id": pond.id,
        "pond_name": pond.pond_name,
        "total_alerts": len(alerts),
        "alerts": alerts
    }

@router.get("/{pond_id}/trends")
def get_pond_trends(
    pond_id: int,
    db: Session = Depends(get_db)
):

    # Find pond
    pond = (
        db.query(PondDB)
        .filter(PondDB.id == pond_id)
        .first()
    )

    if not pond:
        return {
            "error": "Pond not found."
        }

    # Get recent readings
    readings = (
        db.query(PondReadingDB)
        .filter(
            PondReadingDB.pond_name
            == pond.pond_name
        )
        .order_by(
            PondReadingDB.recorded_at.desc()
        )
        .limit(10)
        .all()
    )

    # Trend service expects oldest -> newest
    readings.reverse()

    trend_analysis = analyze_pond_trends(
        readings
    )

    return {
        "pond_id": pond.id,
        "pond_name": pond.pond_name,
        **trend_analysis
    }