import React, { useState } from 'react';
import axios from 'axios';
import './Search.css';

const Search = ({ setArticles }) => {
  const [keyword, setKeyword] = useState('');

  const handleSearch = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.get(`http://localhost:8000/subjects/search?q=${keyword}`);
      setArticles(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="search-container">
      <form onSubmit={handleSearch}>
        <input
          type="text"
          placeholder="Enter keyword"
          value={keyword}
          onChange={(e) => setKeyword(e.target.value)}
        />
        <button type="submit">Search</button>
      </form>
    </div>
  );
};

export default Search;