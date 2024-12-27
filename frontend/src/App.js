// src/App.js
import React from 'react';
import News from './components/News';
import './App.css';

const App = () => {
  return (
    <div className="app-container">
      {/* Colonne de gauche : Articles */}
        <News />
    </div>
  );
};

export default App;
