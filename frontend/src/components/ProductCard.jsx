export default function ProductCard({ product, isAuthenticated, onBuy, isBuying }) {
  const price = product.price?.toFixed(2) ?? "0.00";
  const stock = product.stock ?? 0;

  return (
    <li>
      <strong>{product.name || "Unknown Product"}</strong> — ${price} ({stock} in stock)
      <p>{product.description || "No description available."}</p>
      {isAuthenticated && (
        <button disabled={stock < 1 || isBuying} onClick={() => onBuy(product.id)}>
          {isBuying ? "Buying..." : "Buy 1"}
        </button>
      )}
    </li>
  );
}
