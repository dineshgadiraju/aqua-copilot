from fastapi import FastAPI

from .database import engine
from .db_models import Base

from .routes.ponds import router as ponds_router
from .routes.predictions import router as predictions_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Aqua Copilot API",
    description=(
        "AI-powered shrimp pond health "
        "and risk prediction API"
    ),
    version="0.3.0"
)


app.include_router(ponds_router)
app.include_router(predictions_router)


@app.get("/")
def root():
    return {
        "project": "Aqua Copilot",
        "status": "running",
        "version": "0.3.0",
        "docs": "/docs"
    }