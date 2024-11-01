import requests
from datetime import datetime

def fetch_news(keyword: str):
    # Remplacez par votre propre clé API
    API_KEY = "votre_clé_api_news"
    url = "https://newsapi.org/v2/everything"
    params = {
        'q': keyword,
        'apiKey': API_KEY,
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
                'published_at': datetime.strptime(item.get('publishedAt'), '%Y-%m-%dT%H:%M:%SZ'),
                'url': item.get('url'),
                'subjects': [keyword]
            }
            articles_data.append(article)
    else:
        # Gérer les erreurs
        pass
    return articles_data
