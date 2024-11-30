import pytest
from unittest.mock import patch, MagicMock
from app.services.analyzer_service import Analyzer

def test_analyzer_initialization():
    with patch('app.services.analyzer_service.pipeline') as mock_pipeline:
        mock_pipeline.return_value = MagicMock()
        analyzer = Analyzer(model_name='seara/rubert-tiny2-russian-sentiment')

        mock_pipeline.assert_called_once_with(model='seara/rubert-tiny2-russian-sentiment')
        assert analyzer.model is not None



def test_analyzer_predict_positive():
    with patch('app.services.analyzer_service.pipeline') as mock_pipeline:

        review = "Девочки, смело заказываем"

        mock_model = MagicMock()
        mock_model.return_value = [{'label': 'positive'}]

        mock_pipeline.return_value = mock_model

        analyzer = Analyzer()
        result = analyzer.predict(review)

        assert result == 'positive'
        mock_model.assert_called_once_with(review)



def test_analyzer_predict_negative():
    with patch('app.services.analyzer_service.pipeline') as mock_pipeline:

        review = "Продукт полная туфта!"

        mock_model = MagicMock()
        mock_model.return_value = [{'label': 'negative'}]

        mock_pipeline.return_value = mock_model

        analyzer = Analyzer()
        result = analyzer.predict(review)

        assert result == 'negative'
        mock_model.assert_called_once_with(review)



def test_analyzer_predict_neutral():
    with patch('app.services.analyzer_service.pipeline') as mock_pipeline:

        review = "Я вчера ходил в кино..."

        mock_model = MagicMock()
        mock_model.return_value = [{'label': 'neutral'}]

        mock_pipeline.return_value = mock_model

        analyzer = Analyzer()
        result = analyzer.predict(review)

        assert result == 'neutral'
        mock_model.assert_called_once_with(review)



def test_analyzer_predict_irrelevant():
    with patch('app.services.analyzer_service.pipeline') as mock_pipeline:

        review = "1232131323123 ЫУЧ ЙЗЦЩУЗЙЩОУЗЩЙЦВ"

        mock_model = MagicMock()
        mock_model.return_value = [{'label': 'neutral'}]

        mock_pipeline.return_value = mock_model

        analyzer = Analyzer()
        result = analyzer.predict(review)

        assert result == 'neutral'
        mock_model.assert_called_once_with(review)