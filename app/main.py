from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine

# import ALL models
from app.models import (
    user_model,
    transporter_model,
    shipment_model,
    shipment_assignment_model,
    shipment_status_model,
    handover_model
)

# import routers
from app.routes.admin_routes import router as admin_router
from app.routes.auth_routes import router as auth_router
from app.routes.user_routes import router as user_router
from app.routes.transporter_routes import router as transporter_router
from app.routes.shipment_routes import router as shipment_router
from app.routes.shipment_assignment_routes import router as assignment_router
from app.routes.handover_routes import router as handover_router
from app.routes.status_routes import router as status_router

app = FastAPI()

# ✅ CORS (important for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Create tables
Base.metadata.create_all(bind=engine)

# ✅ THE FIX: Removed extra prefixes that were causing 404s
# Since these routers (like auth_router) already have prefixes defined
# inside their own files, we don't add them again here.
app.include_router(admin_router)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(transporter_router)
app.include_router(shipment_router)
app.include_router(assignment_router)
app.include_router(handover_router)
app.include_router(status_router)

# ✅ Root route
@app.get("/")
def root():
    return {"message": "Backend running 🚀"}