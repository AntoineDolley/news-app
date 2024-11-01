# tests/unit/test_fetch_news.py

from app.utils.fetch_news import fetch_news
from unittest.mock import patch
import pytest

@patch("app.utils.fetch_news.requests.get")
def test_fetch_news_success(mock_get):
    """
    Teste le succès de la récupération des actualités avec un mot-clé valide.
    """
    # Simulation de la réponse de l'API
    mock_response = {
        "articles": [
            {
                "title": "Test Article",
                "description": "This is a test article.",
                "publishedAt": "2023-01-01T12:00:00Z",
                "url": "https://example.com/test-article"
            }
        ]
    }
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_response

    # Appel de la fonction
    articles = fetch_news("test")

    # Vérifications
    assert len(articles) == 1
    article = articles[0]
    assert article["title"] == "Test Article"
    assert article["summary"] == "This is a test article."
    assert article["url"] == "https://example.com/test-article"
    assert article["published_at"] == "2023-01-01T12:00:00"
    assert article["subjects"] == ["test"]

@patch("app.utils.fetch_news.requests.get")
def test_fetch_news_failure(mock_get):
    """
    Teste la gestion des erreurs lors de l'échec de la récupération des actualités.
    """
    # Simulation d'une erreur de l'API
    mock_get.return_value.status_code = 500

    # Appel de la fonction et vérification de l'exception
    with pytest.raises(Exception):
        fetch_news("test")
