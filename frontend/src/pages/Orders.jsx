import { useEffect, useState } from "react";
import { api } from "../api";
import OrderItem from "../components/OrderItem";

export default function Orders() {
  const [orders, setOrders] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    setIsLoading(true);
    api.listOrders()
      .then(setOrders)
      .catch((err) => setError(err.message))
      .finally(() => setIsLoading(false));
  }, []);

  return (
    <div>
      <h2>My Orders</h2>
      {isLoading && <p>Loading orders...</p>}
      {error && <p className="error">{error}</p>}
      
      {!isLoading && !error && orders.length === 0 && (
        <p className="empty-state">No orders found.</p>
      )}

      {!isLoading && orders.length > 0 && (
        <ul className="order-list">
          {orders.map((order) => (
            <OrderItem key={order.id} order={order} />
          ))}
        </ul>
      )}
    </div>
  );
}
