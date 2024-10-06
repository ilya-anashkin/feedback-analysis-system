from fastapi import FastAPI
from app.routes.feedback_routes import router as feedback_router

app = FastAPI()

app.include_router(feedback_router, prefix="/api/feedback")

@app.get("/")
async def main():
    """
    Main endpoint of the Feedback Analysis System.

    Returns:
        dict: A welcome message and information about the Swagger documentation.
    """
    return {
        "message": "Welcome to Feedback Analysis System (FAS)",
        "swagger": "Use /docs route for Swagger"
    }
