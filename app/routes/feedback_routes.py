from fastapi import BackgroundTasks
from fastapi import APIRouter, HTTPException
from app.services.feedback_service import FeedbackService

router = APIRouter()
feedback_service = FeedbackService()

@router.get("/info")
async def info():
    return {
        "connected_to_db": feedback_service.is_connected_to_db,
        "processing": feedback_service.is_processing,
        "config": feedback_service.config,
    }

@router.post("/start")
async def start(background_tasks: BackgroundTasks):
    if feedback_service.is_processing:
        raise HTTPException(status_code=400, detail="Processing is already running")

    try:
        await feedback_service.start_processing(background_tasks)
    except Exception as err:
        raise HTTPException(status_code=500, detail=err)

    return {"message": "Processing started"}

@router.post("/stop")
async def stop():
    if not feedback_service.is_processing:
        raise HTTPException(status_code=400, detail="Processing is not running")

    await feedback_service.stop_processing()
    return {"message": "Processing stopped"}
