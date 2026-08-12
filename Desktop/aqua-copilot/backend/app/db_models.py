from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.sql import func

from .database import Base


class PondDB(Base):
    __tablename__ = "ponds"

    id = Column(Integer, primary_key=True, index=True)

    pond_name = Column(String, unique=True, nullable=False, index=True)
    location = Column(String, nullable=True)
    area_m2 = Column(Float, nullable=True)

    species = Column(String, default="Vannamei", nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )


class PondReadingDB(Base):
    __tablename__ = "pond_readings"

    id = Column(Integer, primary_key=True, index=True)

    pond_name = Column(String, nullable=False)

    temperature_c = Column(Float, nullable=False)
    ph = Column(Float, nullable=False)
    dissolved_oxygen_mg_l = Column(Float, nullable=False)
    salinity_ppt = Column(Float, nullable=False)
    ammonia_mg_l = Column(Float, nullable=False)

    feed_kg_day = Column(Float, nullable=False)
    shrimp_age_days = Column(Integer, nullable=False)
    stocking_density_per_m2 = Column(Float, nullable=False)

    risk_level = Column(String, nullable=False)
    risk_probability = Column(Float, nullable=False)

    recorded_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

class PondAlertDB(Base):
    __tablename__ = "pond_alerts"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    reading_id = Column(
        Integer,
        nullable=False,
        index=True
    )

    pond_name = Column(
        String,
        nullable=False,
        index=True
    )

    parameter = Column(
        String,
        nullable=False
    )

    severity = Column(
        String,
        nullable=False
    )

    message = Column(
        String,
        nullable=False
    )

    action = Column(
        String,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )