from fastapi import FastAPI
from database import engine, Base
from routes import contract

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Quick Contract API",
    description="A FastAPI application for managing contracts",
    version="1.0.0"
)

# Include contract routes
app.include_router(contract.router, prefix="/api/v1", tags=["contracts"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Quick Contract API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"} 