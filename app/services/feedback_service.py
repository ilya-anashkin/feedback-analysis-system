from fastapi import BackgroundTasks
from app.config import settings
from app.database.connection import get_session
import time
from app.logger import logger


class FeedbackService:
    def __init__(self):
        self.session = get_session()
        logger.info("FeedbackService successfully connected to database")
        self.is_connected_to_db = True

        self.is_processing: bool = False
        self.config: dict = {
            "source": settings.source_table,
            "destination": settings.destination_table
        }
        logger.info(f"FeedbackService successfully created with config: {self.config}")

    def start_processing(self):
        self.is_processing = True
        # TODO: Start background task processing

    def stop_processing(self):
        self.is_processing = False
        # TODO: Stop background task processing

    async def process(self):
        # TODO: process function for background task
        pass

