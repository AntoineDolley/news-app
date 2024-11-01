import requests
from datetime import datetime
from typing import List, Dict
from ..config import settings

def fetch_news(keyword: str) -> List[Dict[str, str]]:
    """
    Fetch news articles related to a given keyword using an external news API.

    Parameters:
        keyword (str): The keyword to search for in the news articles.

    Returns:
        List[Dict[str, str]]: A list of articles, each represented as a dictionary containing:
            - title (str): The title of the article.
            - summary (str): A brief description or summary of the article.
            - published_at (str): The date and time the article was published, in ISO 8601 format.
            - url (str): The URL to the full article.
            - subjects (List[str]): A list of subjects associated with the article.

    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.
    """
    url = "https://newsapi.org/v2/everything"
    params = {
        'q': keyword,
        'apiKey': settings.NEWS_API_KEY,
        'language': 'fr'  # Pour obtenir des articles en français
    }
    response = requests.get(url, params=params)
    articles_data = []

    if response.status_code == 200:
        data = response.json()
        for item in data.get('articles', []):
            article = {
                'title': item.get('title'),
                'summary': item.get('description'),
                'published_at': datetime.strptime(item.get('publishedAt'), '%Y-%m-%dT%H:%M:%SZ').isoformat(),
                'url': item.get('url'),
                'subjects': [keyword]
            }
            articles_data.append(article)
    else:
        response.raise_for_status()  # Raises an error if the request was unsuccessful

    return articles_data
