import React, { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import "./css/ProductPage.css";

function ProductPage() {
  const { id } = useParams();
  const [product, setProduct] = useState(null);
  const [notFound, setNotFound] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setProduct(null);
    setNotFound(false);
    setLoading(true);

    fetch(`http://127.0.0.1:8000/api/products/${id}/`)
      .then(res => {
        if (!res.ok) throw new Error("Not found");
        return res.json();
      })
      .then(data => {
        setProduct(data);
        setLoading(false);
      })
      .catch(err => {
        setNotFound(true);
        setLoading(false);
      });
  }, [id]);

  if (loading) return <div className="text-center mt-4">Загрузка...</div>;
  if (notFound) return <div className="text-center mt-4">Товар не найден</div>;

  return (
    <div className="product-container">
      <div className="product-left">
        <img src={product.img_main} alt={product.name} className="main-image" />
      </div>

      <div className="product-right">
        <div className="product-info">
          <p className="brand"><strong>Бренд:</strong> {product.brand}</p>
          <h2>{product.name}</h2>
          <p><strong>Цвет:</strong> {product.color_name}</p>

          {product.other_colors?.length > 0 && (
            <>
              <p><strong>Доступные цвета:</strong></p>
              <div className="color-thumbnails">
                {product.other_colors.map(color => (
                  <Link key={color.id} to={`/product/${color.id}`}>
                    <img
                      src={color.img_main}
                      alt={color.color_name}
                      title={color.color_name}
                      className={`color-thumb ${color.id === product.id ? "active" : ""}`}
                    />
                  </Link>
                ))}
              </div>
            </>
          )}

          {product.sizes?.length > 0 && (
            <div className="sizes">
                <h4>Размеры:</h4>
                <div className="size-grid">
                {product.sizes.map(size => (
                    <div
                    key={size.id}
                    className={`size-box ${!size.in_stock ? "out-of-stock" : ""}`}
                    >
                    <div className="size-main">{size.orig_name}</div>
                    <div className="size-sub">{size.size_name}</div>
                    </div>
                ))}
                </div>
            </div>
        )}

          <div className="description">
            <h4>Описание</h4>
            <p>{product.desc}</p>
          </div>
        </div>

        <div className="price-box">
          <p className="price">{product.price / 100} ₽</p>
          <button className="buy-button">Купить</button>
        </div>
      </div>
    </div>
  );
}

export default ProductPage;
