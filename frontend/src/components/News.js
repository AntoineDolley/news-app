// src/components/News.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Search from './Search';
import './News.css';

const News = () => {
  const [articles, setArticles] = useState([]);

  useEffect(() => {
    const fetchNews = async () => {
      try {
        const response = await axios.get('http://localhost:8000/news');
        // Trier les articles par date de publication décroissante
        const sortedArticles = response.data.sort(
          (a, b) => new Date(b.published_at) - new Date(a.published_at)
        );
        setArticles(sortedArticles);
      } catch (error) {
        console.error(error);
      }
    };

    fetchNews();
  }, []);

  return (
    <div className="news-container">
      <h1>News</h1>
      <Search setArticles={setArticles} />
      <ul className="news-list">
        {articles.map((article) => (
          <li key={article.id} className="news-item">
            <h2>{article.title}</h2>
            <p>{article.summary}</p>
            <p><em>Publié le : {new Date(article.published_at).toLocaleString()}</em></p>
            <a href={article.url} target="_blank" rel="noopener noreferrer">Lire la suite</a>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default News;
