from fastapi import BackgroundTasks
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, text
from sqlalchemy import MetaData, Table, Column, Integer, String
from app.config import settings
from app.database.connection import AsyncSessionLocal, SyncSessionLocal, sync_engine
import asyncio
from app.logger import logger


class FeedbackService:
    def __init__(self):
        self.async_session: sessionmaker = AsyncSessionLocal
        self.sync_session: sessionmaker = SyncSessionLocal
        self.is_connected_to_db: bool = True
        logger.info("FeedbackService successfully connected to database")

        self.is_processing: bool = False
        self.config: dict = {
            "source_table": settings.source_table,
            "source_column_name": settings.source_column_name,
            "destination_table": settings.destination_table,
            "destination_column_name": settings.destination_column_name,
        }

        self.destination_table: Table = None
        self.offset: int = 0
        self.limit: int = 2
        logger.info(f"FeedbackService successfully created with config: {self.config}")

    async def start_processing(self, background_tasks: BackgroundTasks):
        await self.create_destination_table()
        if self.destination_table is None:
            raise RuntimeError("Destination table hasn't been created")

        self.is_processing = True
        background_tasks.add_task(self.process)

    async def stop_processing(self):
        self.is_processing = False
        # TODO: Stop background task processing

    async def process(self):
        while self.is_processing:
            await asyncio.sleep(5)
            await self.process_feedback()

    async def process_feedback(self):
        async with self.async_session() as session:
            query = select(text("id"), text(self.config['source_column_name'])).limit(self.limit).offset(self.offset).select_from(text(self.config['source_table']))
            result = await session.execute(query)
            feedbacks = result.fetchall()

            if feedbacks:
                logger.info(f"Select {len(feedbacks)} feedbacks. Send to process")
                for feedback in feedbacks:
                    feedback_id, feedback_text = feedback
                    logger.debug(f"Processing feedback ID: {feedback_id}, Text: {feedback_text}")

                    # TODO: add to created dest table
                    insert_stmt = self.destination_table.insert().values(
                        source_id=feedback_id,
                        **{self.config['destination_column_name']: feedback_text}
                    )

                    await session.execute(insert_stmt)

                await session.commit()
                logger.info(f"{len(feedbacks)} feedbacks successfully processed")
                self.offset += self.limit
            else:
                logger.info("No feedbacks to process")

    async def create_destination_table(self):
        metadata = MetaData()
        self.destination_table = Table(
            self.config['destination_table'], metadata,
            Column('id', Integer, primary_key=True),
            Column('source_id', Integer),
            Column(self.config['destination_column_name'], String)
        )
        async with self.async_session() as session:
            async with session.begin():
                conn = await session.connection()
                await conn.run_sync(metadata.create_all)
