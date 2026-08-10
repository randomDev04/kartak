import { useEffect, useState } from "react";
import { api } from "../api";
import { useAuth } from "../AuthContext";
import ProductCard from "../components/ProductCard";
import { useNavigate } from "react-router-dom";

export default function Products() {
  const [products, setProducts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");
  const [buyingProductId, setBuyingProductId] = useState(null);
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    setIsLoading(true);
    api.listProducts()
      .then(setProducts)
      .catch((err) => setError(err.message))
      .finally(() => setIsLoading(false));
  }, []);

  async function buyOne(productId) {
    if (buyingProductId) return;
    setMessage("");
    setError("");
    setBuyingProductId(productId);
    try {
      await api.createOrder([{ product_id: productId, quantity: 1 }]);
      setMessage("Order placed successfully!");
      const updated = await api.listProducts();
      setProducts(updated);
    } catch (err) {
      setError(err.message);
    } finally {
      setBuyingProductId(null);
    }
  }

  return (
    <div>
      <h2>Products</h2>
      {isLoading && <p>Loading products...</p>}
      {error && <p className="error">{error}</p>}
      {message && (
        <div className="success" style={{ display: "flex", gap: "1rem", alignItems: "center", marginBottom: "1rem" }}>
          <p>{message}</p>
          <button onClick={() => navigate("/orders")}>View Orders</button>
        </div>
      )}
      
      {!isLoading && !error && products.length === 0 && (
        <p className="empty-state">No products found.</p>
      )}

      {!isLoading && products.length > 0 && (
        <ul className="product-list">
          {products.map((p) => (
            <ProductCard
              key={p.id}
              product={p}
              isAuthenticated={isAuthenticated}
              onBuy={buyOne}
              isBuying={buyingProductId === p.id}
            />
          ))}
        </ul>
      )}
    </div>
  );
}
