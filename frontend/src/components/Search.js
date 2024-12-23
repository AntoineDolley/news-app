// src/components/Search.js
import React, { useState } from 'react';
import axios from 'axios';
import './Search.css';

const Search = ({ setArticles }) => {
  const [keyword, setKeyword] = useState('');

  const handleSearch = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.get(`http://localhost:8000/subjects/search?q=${keyword}`);
      // Trier les articles par date de publication décroissante
      const sortedArticles = response.data.sort(
        (a, b) => new Date(b.published_at) - new Date(a.published_at)
      );
      setArticles(sortedArticles);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="search-container">
      <form onSubmit={handleSearch}>
        <input
          type="text"
          placeholder="Entrez un mot-clé"
          value={keyword}
          onChange={(e) => setKeyword(e.target.value)}
        />
        <button type="submit">Rechercher</button>
      </form>
    </div>
  );
};

export default Search;
