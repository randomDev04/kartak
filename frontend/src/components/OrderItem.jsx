export default function OrderItem({ order }) {
  const dateStr = order.created_at ? new Date(order.created_at).toLocaleString() : "Unknown Date";

  return (
    <li>
      <strong>Order #{order.id}</strong> — {dateStr}
      <ul>
        {order.items?.map((item, idx) => (
          <li key={idx}>
            Product #{item.product_id} × {item.quantity} @ ${(item.unit_price ?? 0).toFixed(2)}
          </li>
        ))}
      </ul>
    </li>
  );
}
