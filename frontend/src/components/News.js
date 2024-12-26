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
      <Search setArticles={setArticles} />
      <ul className="news-list">
        {articles.map((article) => (
          <a href={article.url} className="article-link">
            <li key={article.id} className="news-item">
              <h4 className="news-title">{article.title}</h4>
              <p>{article.summary}</p>
              <p><em>Publié le : {new Date(article.published_at).toLocaleString()}</em></p>
            </li>
          </a>
        ))}
      </ul>
    </div>
  );
};

export default News;
