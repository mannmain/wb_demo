import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import "./css/Header.css";

export default function Header({ onSearch, searchValue }) {
  const [searchText, setSearchText] = useState(searchValue || '');
  const navigate = useNavigate();

  useEffect(() => {
    setSearchText(searchValue);
  }, [searchValue]);

  function handleChange(e) {
    setSearchText(e.target.value);
  }

  function handleSearch(e) {
    e.preventDefault();
    onSearch(searchText.trim());
    navigate('/');
  }

  return (
    <header className="header j-header">
      <div className="header__container">
        {/* <span className="logo">WildBerries</span> */}
        <Link to="/" className="logo">
          WildBerries
        </Link>
        <form className="search-bar" onSubmit={handleSearch}>
          <input
            type="text"
            className="search-input"
            placeholder="Поиск товаров..."
            value={searchText}
            onChange={handleChange}
          />
          <button className="search-btn" type="submit">Найти</button>
        </form>
      </div>
    </header>
  );
}
