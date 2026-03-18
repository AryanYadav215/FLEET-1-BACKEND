from fastapi import FastAPI

from app.database import Base, engine
from app.routes import shipment_assignment_routes
from app.routes.auth_routes import router as auth_router
from app.routes.user_routes import router as user_router
from app.routes.transporter_routes import router as transporter_router

from app.database import Base, engine
from app.models import transporter_model, user_model

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(transporter_router)
app.include_router(shipment_assignment_routes.router)