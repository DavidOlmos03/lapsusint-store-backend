from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import license_router, user_router, auth_router
from app.db.dynamodb import dynamodb
from app.core.config import settings

app = FastAPI(title="LapsusINt Store Backend", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React default port
        "http://localhost:3001",  # Alternative React port
        "http://localhost:8080",  # Vue default port
        "http://localhost:4200",  # Angular default port
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "http://127.0.0.1:8080",
        "http://127.0.0.1:4200",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(license_router)
app.include_router(user_router)
app.include_router(auth_router)

@app.on_event("startup")
async def startup_db_client():
    dynamodb.connect_to_dynamodb()
    dynamodb.create_tables()

@app.on_event("shutdown")
async def shutdown_db_client():
    # DynamoDB doesn't need explicit connection closing
    pass

@app.get("/")
def root():
    return {"message": "Welcome to LapsusINt Store Backend API"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "LapsusINt Store Backend"} 