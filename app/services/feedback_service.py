import asyncio

from fastapi import BackgroundTasks
from sqlalchemy import Column, Integer, MetaData, String, Table, select, text
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.database.connection import AsyncSessionLocal, SyncSessionLocal
from app.logger import logger
from app.services.analyzer_service import Analyzer


class FeedbackService:
    """
    FeedbackService class to manage feedback processing.
    """

    def __init__(self):
        """Initializes FeedbackService and checks database connection."""
        self.async_session: sessionmaker = AsyncSessionLocal
        """Asynchronous session maker for database interactions."""
        self.sync_session: sessionmaker = SyncSessionLocal
        """Synchronous session maker for database interactions."""
        self.is_connected_to_db: bool = True
        """Indicates if the service is connected to the database."""
        logger.info("FeedbackService successfully connected to database")

        self.analyzer: Analyzer = Analyzer()
        logger.info("AnalyzerService successfully loaded")

        self.is_processing: bool = False
        """Indicates if feedback processing is currently running."""
        self.config: dict = {
            "source_table": settings.source_table,
            "source_column_name": settings.source_column_name,
            "destination_table": settings.destination_table,
            "destination_column_name": settings.destination_column_name,
        }
        """Configuration settings for source and destination tables and columns."""

        self.destination_table: Table = None
        """SQLAlchemy Table object for the destination table."""
        self.offset: int = 0
        """Offset for pagination during feedback processing."""
        self.limit: int = 2
        """Limit for the number of feedback records to process at a time."""
        logger.info(f"FeedbackService successfully created with config: {self.config}")

    async def start_processing(self, background_tasks: BackgroundTasks):
        """
        Start processing feedback in the background.

        This method creates the destination table and starts the feedback processing task.

        Args:
            background_tasks (BackgroundTasks): FastAPI utility to run tasks in the background.

        Raises:
            RuntimeError: If the destination table has not been created.
        """
        await self.create_destination_table()
        if self.destination_table is None:
            raise RuntimeError("Destination table hasn't been created")

        self.is_processing = True
        background_tasks.add_task(self.process)

    async def stop_processing(self):
        """Stop the feedback processing."""
        self.is_processing = False

    async def process(self):
        """
        Continuously process feedback while processing is enabled.

        This method runs in a loop, calling the process_feedback method every 5 seconds.
        """
        while self.is_processing:
            await asyncio.sleep(5)
            await self.process_feedback()

    async def process_feedback(self):
        """
        Fetch and process feedback from the source table.

        This method retrieves feedback records from the source table and
        inserts them into the destination table. Logging is performed to
        track the number of records processed.

        If no feedbacks are found, an info log is generated.
        """
        async with self.async_session() as session:
            query = (
                select(text("id"), text(self.config["source_column_name"]))
                .limit(self.limit)
                .offset(self.offset)
                .select_from(text(self.config["source_table"]))
            )
            result = await session.execute(query)
            feedbacks = await result.fetchall()  # Добавлено await

            if feedbacks:
                logger.info(f"Select {len(feedbacks)} feedbacks. Send to process")
                for feedback in feedbacks:
                    feedback_id, feedback_text = feedback
                    logger.debug(
                        f"Processing feedback ID: {feedback_id}, Text: {feedback_text}"
                    )

                    tonality = self.analyzer.predict(feedback_text)

                    insert_stmt = self.destination_table.insert().values(
                        source_id=feedback_id,
                        **{self.config["destination_column_name"]: feedback_text},
                        tonality=tonality,
                    )

                    await session.execute(insert_stmt)

                await session.commit()
                logger.info(f"{len(feedbacks)} feedbacks successfully processed")
                self.offset += self.limit
            else:
                logger.info("No feedbacks to process")

    async def create_destination_table(self):
        """
        Create the destination table in the database.

        This method defines the schema for the destination table and
        creates it in the database if it does not already exist.
        """
        metadata = MetaData()
        self.destination_table = Table(
            self.config["destination_table"],
            metadata,
            Column("id", Integer, primary_key=True),
            Column("source_id", Integer),
            Column(self.config["destination_column_name"], String),
            Column("tonality", String),
        )
        async with self.async_session() as session:
            async with session.begin():
                conn = await session.connection()
                await conn.run_sync(metadata.create_all)
