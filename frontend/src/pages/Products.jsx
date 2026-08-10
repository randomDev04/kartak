import { useEffect, useState } from "react";
import { api } from "../api";
import { useAuth } from "../AuthContext";
import ProductCard from "../components/ProductCard";

export default function Products() {
  const [products, setProducts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");
  const { isAuthenticated } = useAuth();

  useEffect(() => {
    setIsLoading(true);
    api.listProducts()
      .then(setProducts)
      .catch((err) => setError(err.message))
      .finally(() => setIsLoading(false));
  }, []);

  async function buyOne(productId) {
    setMessage("");
    setError("");
    try {
      await api.createOrder([{ product_id: productId, quantity: 1 }]);
      setMessage("Order placed!");
      const updated = await api.listProducts();
      setProducts(updated);
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div>
      <h2>Products</h2>
      {isLoading && <p>Loading products...</p>}
      {error && <p className="error">{error}</p>}
      {message && <p className="success">{message}</p>}
      {!isLoading && (
        <ul className="product-list">
          {products.map((p) => (
            <ProductCard
              key={p.id}
              product={p}
              isAuthenticated={isAuthenticated}
              onBuy={buyOne}
            />
          ))}
        </ul>
      )}
    </div>
  );
}
