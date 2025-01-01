
# News Clustering and Summarization API

This project is a **FastAPI** application designed to fetch, cluster, and summarize news articles. It integrates with OpenAI's API for generating embeddings and summaries, and provides a user-friendly frontend to display news and their clusters.

---

## Features

- **Fetch News**: Fetch articles from a news API and store them in a PostgreSQL database.
- **Embeddings**: Use OpenAI's embedding model to generate vector representations for articles.
- **Clustering**: Perform clustering on articles based on their embeddings to identify similar topics.
- **Summarization**: Summarize clusters and individual articles using OpenAI's GPT model.
- **Frontend**: React-based interface displaying articles and their clusters.

---

## Technologies Used

### Backend
- **FastAPI**: Main framework for building the API.
- **SQLAlchemy**: ORM for managing the database.
- **PostgreSQL**: Database for storing articles and embeddings.
- **pgvector**: Extension for handling vector data in PostgreSQL.
- **OpenAI API**: For embeddings and summarization.
- **News API**: To retrieve news articles.

### Frontend
- **React**: Frontend library for building the UI.
- **Axios**: For making API requests to the backend.

### Infrastructure
- **Docker**: Containerize the application for easy deployment.
- **APScheduler**: Scheduler for periodic tasks such as fetching news.

---

## API Endpoints

### News Endpoints

1. **GET `/news`**
   - Fetch the latest news articles from the database.
   - Returns articles and their clusters.

2. **GET `/subjects/search?q={query}`**
   - Search for articles similar to the query using vector similarity.
   - Returns articles and their clusters.

---

## Setup Instructions

### Prerequisites
- Python 3.10+
- Docker
- Node.js & npm (for the frontend)

### Clone the Repository
```bash
git clone https://github.com/yourusername/news-clustering.git
cd news-clustering
```

### Backend Setup
1. Create a `.env` file in the `backend/` directory:
    ```env
    DATABASE_URL=postgresql://user:password@localhost/news_db
    OPENAI_API_KEY=your_openai_api_key
    NEWS_API_KEY=your_news_api_key
    SECRET_KEY=news-app
    ```

Start the backend with Docker:
    ```bash
    docker-compose up --build
    ```
    
---

## How It Works

### Workflow Overview

1. **Fetching Articles**:
    - The backend periodically fetches news articles using a scheduler.
    - Articles are stored in the database with their embeddings.

2. **Clustering**:
    - Articles are clustered using KMeans based on their embeddings.
    - Clusters are summarized, and titles are generated for each cluster.

3. **Serving Data**:
    - The API serves articles and clusters to the frontend.

4. **Frontend Display**:
    - Articles are displayed in the main panel.
    - Clusters are displayed in a side panel for quick navigation.

---

## Screenshots

### Frontend Interface

#### Main View
- Articles displayed on the left.
- Clusters displayed on the right.

#### Cluster Detail
- Clicking a cluster shows the articles in that cluster.

---

## Future Enhancements

- **Improved Clustering**: Experiment with different clustering algorithms.
- **Advanced Search**: Support for advanced query operators.
- **User Authentication**: Allow users to save and track articles or clusters.
- **Dashboard**: Provide insights into trending topics and articles.

---

## License

This project is licensed under the MIT License.
