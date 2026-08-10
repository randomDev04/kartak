export default function ProductCard({ product, isAuthenticated, onBuy }) {
  const price = product.price?.toFixed(2) ?? "0.00";
  const stock = product.stock ?? 0;

  return (
    <li>
      <strong>{product.name || "Unknown Product"}</strong> — ${price} ({stock} in stock)
      <p>{product.description || "No description available."}</p>
      {isAuthenticated && (
        <button disabled={stock < 1} onClick={() => onBuy(product.id)}>
          Buy 1
        </button>
      )}
    </li>
  );
}
