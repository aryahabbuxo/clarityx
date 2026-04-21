import { useState } from "react";

function App() {
  const [barcode, setBarcode] = useState("");
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [weights, setWeights] = useState([0.25, 0.25, 0.25, 0.25]);

  const labels = ["Sustainability", "Health", "Transparency", "Social"];

  const updateWeight = (index, newVal) => {
    const val = parseFloat(newVal);
    const remaining = 1 - val;
    const otherTotal = weights.reduce((s, w, i) => i !== index ? s + w : s, 0);
    const newWeights = weights.map((w, i) => {
      if (i === index) return val;
      if (otherTotal === 0) return remaining / 3;
      return parseFloat(((w / otherTotal) * remaining).toFixed(2));
    });
    setWeights(newWeights);
  };

  const search = async () => {
    if (!barcode) return;
    setLoading(true);
    setError("");
    setProduct(null);
    try {
      const res = await fetch(
        `http://127.0.0.1:8080/product/${barcode}?w1=${weights[0]}&w2=${weights[1]}&w3=${weights[2]}&w4=${weights[3]}`
      );
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
    <div style={{ maxWidth: 620, margin: "40px auto", fontFamily: "sans-serif", padding: "0 20px" }}>
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

      <div style={{ border: "1px solid #ddd", borderRadius: 12, padding: 20, marginBottom: 24, background: "#f9fdf9" }}>
        <h3 style={{ margin: "0 0 16px", fontSize: 15 }}>Your priorities (adjust before searching)</h3>
        {labels.map((label, i) => (
          <div key={label} style={{ marginBottom: 12 }}>
            <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 4 }}>
              <span style={{ fontSize: 14 }}>{label}</span>
              <span style={{ fontSize: 14, fontWeight: "bold" }}>{Math.round(weights[i] * 100)}%</span>
            </div>
            <input
              type="range" min="0.05" max="0.85" step="0.01"
              value={weights[i]}
              onChange={e => updateWeight(i, e.target.value)}
              style={{ width: "100%" }}
            />
          </div>
        ))}
        <p style={{ fontSize: 12, color: "#888", margin: "8px 0 0" }}>
          Total: {Math.round(weights.reduce((s, w) => s + w, 0) * 100)}% — sliders auto-balance
        </p>
      </div>

      {loading && <p>Loading...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {product && (
        <div style={{ border: "1px solid #ddd", borderRadius: 12, padding: 24 }}>
          <h2 style={{ margin: "0 0 4px" }}>{product.name}</h2>
          <p style={{ color: "#888", margin: "0 0 20px" }}>{product.brand}</p>

          <h3 style={{ margin: "0 0 12px" }}>Scores</h3>
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
            <strong>Composite Score (WASPAS): {product.composite}/100</strong>
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