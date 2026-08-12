from fastapi import FastAPI
from app.config import settings
from app.api.v1.parking_spaces import router as parking_spaces_router
from app.api.v1.reservations import router as reservations_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API for managing parking spaces and handling slot reservations.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

#register API Routers
app.include_router(parking_spaces_router, prefix="/api/v1")
app.include_router(reservations_router, prefix="/api/v1")


@app.get("/health", tags=["Health Check"])
def health_check():
    #verify if API service is running
    return {"status": "ok", "project": settings.PROJECT_NAME}