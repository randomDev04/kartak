import { useEffect, useState } from "react";
import { api } from "../api";

export default function Orders() {
  const [orders, setOrders] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    api.listOrders().then(setOrders).catch((err) => setError(err.message));
  }, []);

  return (
    <div>
      <h2>My Orders</h2>
      {error && <p className="error">{error}</p>}
      {orders.length === 0 && !error && <p>No orders yet.</p>}
      <ul className="order-list">
        {orders.map((order) => (
          <li key={order.id}>
            <strong>Order #{order.id}</strong> — {new Date(order.created_at).toLocaleString()}
            <ul>
              {order.items.map((item, idx) => (
                <li key={idx}>
                  Product #{item.product_id} × {item.quantity} @ ${item.unit_price.toFixed(2)}
                </li>
              ))}
            </ul>
          </li>
        ))}
      </ul>
    </div>
  );
}
