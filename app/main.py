from fastapi import FastAPI
from app.database import Base, engine

# import ALL models
from app.models import (
    user_model,
    transporter_model,
    shipment_model,
    shipment_assignment_model,
    shipment_status_model
)

from app.routes.auth_routes import router as auth_router
from app.routes.user_routes import router as user_router
from app.routes.transporter_routes import router as transporter_router
from app.routes.shipment_routes import router as shipment_router
from app.routes.shipment_assignment_routes import router as assignment_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(transporter_router)
app.include_router(shipment_router)
app.include_router(assignment_router)

@app.get("/")
def root():
    return {"message": "Backend running 🚀"}