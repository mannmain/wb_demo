import React from 'react';
import "./css/Pagination.css";

export default function Pagination({ page, totalPages, onPageChange }) {
  return (
    <div className="pagination">
      <button
        className="btn"
        onClick={() => onPageChange(page - 1)}
        disabled={page <= 1}
      >
        Назад
      </button>

      <span className="pageInfo">
        Страница {page} из {totalPages}
      </span>

      <button
        className="btn"
        onClick={() => onPageChange(page + 1)}
        disabled={page >= totalPages}
      >
        Вперед
      </button>
    </div>
  );
}
