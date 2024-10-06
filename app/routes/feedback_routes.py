from fastapi import BackgroundTasks
from fastapi import APIRouter, HTTPException
from app.services.feedback_service import FeedbackService

router = APIRouter()
feedback_service = FeedbackService()

@router.get("/info")
async def info():
    """
    Get the current status of the feedback processing service.

    Returns:
        dict: A dictionary containing the connection status to the database,
              whether processing is ongoing, and the current configuration
              of the feedback service.
    """
    return {
        "connected_to_db": feedback_service.is_connected_to_db,
        "processing": feedback_service.is_processing,
        "config": feedback_service.config,
    }

@router.post("/start")
async def start(background_tasks: BackgroundTasks):
    """
    Start the feedback processing service.

    This endpoint triggers the processing of feedback in the background.

    Args:
        background_tasks (BackgroundTasks): A FastAPI utility that allows
                                             tasks to run in the background.

    Raises:
        HTTPException:
            - 400: If processing is already running.
            - 500: If an error occurs during processing.

    Returns:
        dict: A message indicating that processing has started.
    """
    if feedback_service.is_processing:
        raise HTTPException(status_code=400, detail="Processing is already running")

    try:
        await feedback_service.start_processing(background_tasks)
    except Exception as err:
        raise HTTPException(status_code=500, detail=err)

    return {"message": "Processing started"}

@router.post("/stop")
async def stop():
    """
    Stop the feedback processing service.

    This endpoint stops the ongoing feedback processing.

    Raises:
        HTTPException:
            - 400: If processing is not currently running.

    Returns:
        dict: A message indicating that processing has been stopped.
    """
    if not feedback_service.is_processing:
        raise HTTPException(status_code=400, detail="Processing is not running")

    await feedback_service.stop_processing()
    return {"message": "Processing stopped"}
