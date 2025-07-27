from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # Frontend dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include contract routes
app.include_router(contract.router, prefix="/api/v1", tags=["contracts"])

# Add health endpoint under API v1 prefix
@app.get("/api/v1/health")
def health_check_api():
    return {"status": "healthy"}

@app.get("/")
def read_root():
    return {"message": "Welcome to Quick Contract API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"} 