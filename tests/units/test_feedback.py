import asyncio
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.services.feedback_service import FeedbackService


@pytest.fixture
def feedback_service():
    """Создает экземпляр FeedbackService с замоканным конфигом."""
    mock_settings = MagicMock(
        db_host="localhost",
        db_port="5432",
        db_name="test_db",
        db_user="test_user",
        db_password="test_password",
        source_table="test_source_table",
        source_column_name="feedback_text",
        destination_table="test_destination_table",
        destination_column_name="processed_feedback",
    )

    with patch("app.config.settings", new=mock_settings):
        service = FeedbackService()
        service.destination_table = MagicMock()  # Фиктивная таблица для тестов
        return service


@pytest.mark.asyncio
async def test_start_processing(feedback_service):
    """Тестирует метод start_processing."""
    background_tasks = MagicMock()

    # Мокаем методы
    feedback_service.create_destination_table = AsyncMock()
    feedback_service.process = AsyncMock()

    # Вызов метода
    await feedback_service.start_processing(background_tasks)

    # Проверки
    feedback_service.create_destination_table.assert_awaited_once()
    background_tasks.add_task.assert_called_once_with(feedback_service.process)
    assert feedback_service.is_processing is True


@pytest.mark.asyncio
async def test_stop_processing(feedback_service):
    """Тестирует метод stop_processing."""
    feedback_service.is_processing = True

    # Вызов метода
    await feedback_service.stop_processing()

    # Проверки
    assert feedback_service.is_processing is False


@pytest.mark.asyncio
async def test_process(feedback_service):
    """Тестирует процессинг с фиктивными данными."""
    feedback_service.is_processing = True
    feedback_service.process_feedback = AsyncMock()

    # Останавливаем процесс через 1 итерацию
    async def stop_after_one_iteration():
        await asyncio.sleep(5)
        feedback_service.is_processing = False

    feedback_service.process_feedback.side_effect = stop_after_one_iteration

    await feedback_service.process()

    # Проверки
    feedback_service.process_feedback.assert_awaited()


@pytest.mark.asyncio
async def test_process_feedback(feedback_service):
    """Тестирует метод process_feedback."""
    feedback_service.analyzer = MagicMock()
    feedback_service.analyzer.predict.return_value = "positive"

    session_mock = AsyncMock()
    session_mock.__aenter__.return_value.execute.return_value.fetchall = AsyncMock(
        return_value=[
            (1, "Отличный продукт!"),
            (2, "Не очень понравилось."),
        ]
    )
    feedback_service.async_session = MagicMock(return_value=session_mock)

    table_mock = MagicMock()
    table_mock.insert.return_value.values = MagicMock()
    feedback_service.destination_table = table_mock  # Мокаем destination_table

    await feedback_service.process_feedback()

    # Убедитесь, что метод insert был вызван
    table_mock.insert.assert_called()

@pytest.mark.asyncio
async def test_create_destination_table(feedback_service):
    """Тестирует метод create_destination_table."""
    # Настройка моков
    session_mock = AsyncMock()
    session_mock.connection = AsyncMock()
    connection_mock = AsyncMock()
    session_mock.connection.return_value = connection_mock
    connection_mock.run_sync = MagicMock()

    # Настройка асинхронного контекстного менеджера для сессии
    session_mock.__aenter__.return_value = session_mock
    feedback_service.async_session = MagicMock(return_value=session_mock)





