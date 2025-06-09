import React, { useEffect, useState } from 'react';
import "./css/Filter.css";

export default function Filters({ onApply }) {
  const [brands, setBrands] = useState([]);
  const [colors, setColors] = useState([]);
  const [kinds, setKinds] = useState([]);

  const [brand, setBrand] = useState('');
  const [color, setColor] = useState('');
  const [kind, setKind] = useState('');
  const [priceMin, setPriceMin] = useState('');
  const [priceMax, setPriceMax] = useState('');
  const [ordering, setOrdering] = useState('');


  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/brands/')
      .then(res => res.json())
      .then(data => {
        console.log('brands API response:', data);
        setBrands(data);
      })
      .catch(console.error);

    fetch('http://127.0.0.1:8000/api/colors/')
      .then(res => res.json())
      .then(data => setColors(data))
      .catch(console.error);

    fetch('http://127.0.0.1:8000/api/kinds/')
      .then(res => res.json())
      .then(data => setKinds(data))
      .catch(console.error);
  }, []);

  function applyFilters() {
    onApply({
      brand,
      color,
      kind,
      ordering,
      priceMin: priceMin ? (parseInt(priceMin) * 100).toString() : '',
      priceMax: priceMax ? (parseInt(priceMax) * 100).toString() : '',
    });
  }

  return (
    <div className="filters">
      <select value={brand} onChange={e => setBrand(e.target.value)}>
        <option value="">Все бренды</option>
        {brands.map(b => <option key={b.id} value={b.brand}>{b.brand}</option>)}
      </select>

      <select value={color} onChange={e => setColor(e.target.value)}>
        <option value="">Все цвета</option>
        {colors.map(c => <option key={c.id} value={c.name}>{c.name}</option>)}
      </select>

      <select value={kind} onChange={e => setKind(e.target.value)}>
        <option value="">Все виды</option>
        {kinds.map(k => <option key={k.id} value={k.name}>{k.name}</option>)}
      </select>

      <input
        type="number"
        placeholder="Мин. цена"
        value={priceMin}
        onChange={e => setPriceMin(e.target.value)}
      />
      <input
        type="number"
        placeholder="Макс. цена"
        value={priceMax}
        onChange={e => setPriceMax(e.target.value)}
      />

      <select value={ordering} onChange={e => setOrdering(e.target.value)}>
        <option value="">Сортировка</option>
        <option value="name">По имени ⬆</option>
        <option value="-name">По имени ⬇</option>
        <option value="brand">По бренду ⬆</option>
        <option value="-brand">По бренду ⬇</option>
        <option value="price">По цене ⬆</option>
        <option value="-price">По цене ⬇</option>
      </select>

      <button onClick={applyFilters}>Применить</button>
    </div>
  );
}
