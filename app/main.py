from fastapi import FastAPI
from app.database import Base, engine

# Import ALL models so SQLAlchemy registers them
from app.models import shipment_model, transporter_model, user_model

# Import routers
from app.routes.auth_routes import router as auth_router
from app.routes.user_routes import router as user_router
from app.routes.transporter_routes import router as transporter_router
from app.routes.shipment_routes import router as shipment_router
from app.routes import shipment_assignment_routes

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(transporter_router)
app.include_router(shipment_router)
app.include_router(shipment_assignment_routes.router)

@app.get("/")
def root():
    return {"message": "Hello"}