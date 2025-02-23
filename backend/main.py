from fastapi import FastAPI
from backend.routers import auth  # Import the new auth router

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to DevGuard API"}

# Include authentication routes
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])

