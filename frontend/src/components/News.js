// src/components/News.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Search from './Search';
import './News.css';

const News = () => {
  const [articles, setArticles] = useState([]);
  const [clusters, setClusters] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchNews = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.get('http://localhost:8000/news'); // ou '/subjects/search?q=...'
      const sortedArticles = response.data.articles.sort(
        (a, b) => new Date(b.published_at) - new Date(a.published_at)
      );
      setArticles(sortedArticles);
      setClusters(response.data.clusters);
    } catch (error) {
      console.error(error);
      setError('Erreur lors de la récupération des articles.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchNews();
  }, []);

  return (
    <div className="news-container">
      <Search setArticles={setArticles} setClusters={setClusters} />
      
      {loading && <p>Chargement des articles...</p>}
      {error && <p className="error">{error}</p>}
      
      {!loading && !error && (
        <div className="content">
          {/* Colonne de gauche : Articles */}
          <div className="articles-panel">
            <h2>Articles Récents</h2>
            <ul className="news-list">
              {articles.map((article) => (
                <a href={article.url} className="article-link" key={article.id}>
                  <li className="news-item">
                    <h3 className="news-title">{article.title}</h3>
                    <p>{article.summary}</p>
                    <p><em>Publié le : {new Date(article.published_at).toLocaleString()}</em></p>
                  </li>
                </a>
              ))}
            </ul>
          </div>

          {/* Colonne de droite : Clusters */}
          <div className="clusters-panel">
            <h2>Clusters</h2>
            {clusters.map((cluster) => (
              <div key={cluster.cluster_id} className="cluster">
                <h3>{cluster.title}</h3>
                <p>{cluster.summary}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default News;
