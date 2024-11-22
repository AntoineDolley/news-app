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
        setArticles(response.data);
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
            <a href={article.url} target="_blank" rel="noopener noreferrer">Read more</a>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default News;