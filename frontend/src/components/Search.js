// src/components/Search.js
import React, { useState } from 'react';
import axios from 'axios';
import './Search.css';

const Search = ({ setArticles, setClusters }) => {
  const [query, setQuery] = useState('');

  const handleSearch = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.get(`http://localhost:8000/subjects/search?q=${query}`);
      const sortedArticles = response.data.articles.sort(
        (a, b) => new Date(b.published_at) - new Date(a.published_at)
      );
      setArticles(sortedArticles);
      setClusters(response.data.clusters);
    } catch (error) {
      console.error(error);
      // Vous pouvez également gérer les erreurs en définissant un état d'erreur spécifique pour le composant Search
    }
  };

  return (
    <form onSubmit={handleSearch} className="search-form">
      <input 
        type="text" 
        value={query} 
        onChange={(e) => setQuery(e.target.value)} 
        placeholder="Rechercher des articles..." 
        className="search-input"
      />
      <button type="submit" className="search-button">Rechercher</button>
    </form>
  );
};

export default Search;
