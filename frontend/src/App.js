import { useState } from "react";

function App() {
  const [barcode, setBarcode] = useState("");
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const search = async () => {
    if (!barcode) return;
    setLoading(true);
    setError("");
    setProduct(null);
    try {
      const res = await fetch(`http://127.0.0.1:8080/product/${barcode}`);
      const data = await res.json();
      if (data.error) {
        setError("Product not found. Try another barcode.");
      } else {
        setProduct(data);
      }
    } catch (e) {
      setError("Could not connect to server.");
    }
    setLoading(false);
  };

  return (
    <div style={{ maxWidth: 600, margin: "40px auto", fontFamily: "sans-serif", padding: "0 20px" }}>
      <h1 style={{ color: "#1a5c3a" }}>🌿 ClarityX</h1>
      <p style={{ color: "#555" }}>Product sustainability transparency platform</p>

      <div style={{ display: "flex", gap: 8, marginBottom: 24 }}>
        <input
          style={{ flex: 1, padding: "10px 14px", fontSize: 16, border: "1px solid #ccc", borderRadius: 8 }}
          placeholder="Enter barcode e.g. 3017620422003"
          value={barcode}
          onChange={e => setBarcode(e.target.value)}
          onKeyDown={e => e.key === "Enter" && search()}
        />
        <button
          style={{ padding: "10px 20px", background: "#1a5c3a", color: "white", border: "none", borderRadius: 8, fontSize: 16, cursor: "pointer" }}
          onClick={search}
        >
          Search
        </button>
      </div>

      {loading && <p>Loading...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {product && (
        <div style={{ border: "1px solid #ddd", borderRadius: 12, padding: 24 }}>
          <h2 style={{ margin: "0 0 4px" }}>{product.name}</h2>
          <p style={{ color: "#888", margin: "0 0 20px" }}>{product.brand}</p>

          <h3>Scores</h3>
          {Object.entries(product.scores).map(([key, val]) => (
            <div key={key} style={{ marginBottom: 12 }}>
              <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 4 }}>
                <span style={{ textTransform: "capitalize" }}>{key}</span>
                <span style={{ fontWeight: "bold" }}>{val}/100</span>
              </div>
              <div style={{ background: "#eee", borderRadius: 4, height: 8 }}>
                <div style={{ width: `${val}%`, height: 8, borderRadius: 4, background: val > 60 ? "#1a5c3a" : val > 40 ? "#f0a500" : "#d9534f" }} />
              </div>
            </div>
          ))}

          <div style={{ marginTop: 20, padding: 16, background: "#f9f9f9", borderRadius: 8 }}>
            <strong>Composite Score: {product.composite}/100</strong>
          </div>

          <div style={{ marginTop: 12, padding: 16, borderRadius: 8, background: product.greenwashing.risk === "Low" ? "#e8f5e9" : product.greenwashing.risk === "Medium" ? "#fff8e1" : "#ffebee" }}>
            <strong>Greenwashing Risk: {product.greenwashing.risk}</strong>
            <p style={{ margin: "4px 0 0", fontSize: 14 }}>{product.greenwashing.reason}</p>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;