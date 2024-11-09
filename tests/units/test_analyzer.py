import pytest
from unittest.mock import patch, MagicMock
from app.services.analyzer_service import Analyzer

def test_analyzer_initialization():
    with patch('app.services.analyzer_service.pipeline') as mock_pipeline:
        mock_pipeline.return_value = MagicMock()
        analyzer = Analyzer(model_name='seara/rubert-tiny2-russian-sentiment')

        mock_pipeline.assert_called_once_with(model='seara/rubert-tiny2-russian-sentiment')
        assert analyzer.model is not None

def test_predict():
    with patch('app.services.analyzer_service.pipeline') as mock_pipeline:
        mock_model = MagicMock()
        mock_model.return_value = [{'label': 'positive'}]

        mock_pipeline.return_value = mock_model

        analyzer = Analyzer()
        result = analyzer.predict("Это отличный продукт!")

        assert result == 'positive'
        mock_model.assert_called_once_with("Это отличный продукт!")

