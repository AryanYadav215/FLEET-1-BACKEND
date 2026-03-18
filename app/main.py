from fastapi import FastAPI
from app.database import engine, Base

# 1. WE MUST IMPORT THE MODELS HERE!
# This makes SQLAlchemy "see" them before it creates the tables.
from app.models import shipment_model

# Import routers
from app.routes.auth_routes import router as auth_router
from app.routes.shipment_routes import router as shipment_router

# 2. Now when this runs, it will finally create the missing 'shipments' table!
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router)
app.include_router(shipment_router)

@app.get("/")
def root():
    return {"message": "Hello"}