// src/App.js
import React from 'react';
import News from './components/News';
import './App.css';

const App = () => {
  return (
    <div className="app-container">
      {/* Colonne de gauche : Articles */}
      <div className="left-column">
        <News />
      </div>
      
      {/* Colonne de droite : Vide pour l'instant */}
      <div className="right-column">
        <h2>Espace à remplir</h2>
        <p>Rien ici pour l'instant.</p>
      </div>
    </div>
  );
};

export default App;
