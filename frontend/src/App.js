import { useState } from "react";
import BarcodeScanner from "./BarcodeScanner";

const GREEN_DARK = "#1e3d2f";
const GREEN_MID = "#2d6a4f";
const GREEN_ACCENT = "#3a8a5a";
const GREEN_LIGHT = "#e8f5e0";
const GREEN_MUTED = "#6aaa7e";
const BG = "#f5f6f0";

const CATALOGUE_PRODUCTS = [
  { name: "Organic Green Tea", brand: "EcoLeaf", category: "Beverages", scores: { sustainability: 92, health: 89, transparency: 84, social: 83 }, waspas: 87, risk: "Low", longevity: "High" },
  { name: "Reusable Water Bottle", brand: "HydroSave", category: "Lifestyle", scores: { sustainability: 95, health: 88, transparency: 90, social: 91 }, waspas: 85, risk: "Low", longevity: "High" },
  { name: "Zero Shampoo Bar", brand: "PureRoots", category: "Personal Care", scores: { sustainability: 81, health: 75, transparency: 78, social: 78 }, waspas: 78, risk: "Medium", longevity: "Good" },
  { name: "Nutella Hazelnut Spread", brand: "Ferrero", category: "Food", scores: { sustainability: 35, health: 65, transparency: 100, social: 50 }, waspas: 62, risk: "Medium", longevity: "Good" },
  { name: "Ecover Washing Liquid", brand: "Ecover", category: "Household", scores: { sustainability: 91, health: 84, transparency: 79, social: 88 }, waspas: 86, risk: "Low", longevity: "High" },
  { name: "Tony's Chocolonely Dark", brand: "Tony's", category: "Confectionery", scores: { sustainability: 74, health: 65, transparency: 92, social: 95 }, waspas: 83, risk: "Low", longevity: "Good" },
];

const DB_STATS = [
  { val: "10,000+", label: "Products Verified" },
  { val: "95%", label: "Accuracy Rate" },
  { val: "500K+", label: "Scans Performed" },
  { val: "50+", label: "Partner Brands" },
];

function scoreColor(v) {
  if (v >= 70) return GREEN_ACCENT;
  if (v >= 50) return "#c57200";
  return "#b83232";
}

function riskStyle(risk) {
  if (risk === "Low") return { bg: "#d4edda", color: "#1a5c3a" };
  if (risk === "Medium") return { bg: "#fff3cd", color: "#856404" };
  return { bg: "#f8d7da", color: "#721c24" };
}

function cap(str) {
  return str.charAt(0).toUpperCase() + str.slice(1);
}

function LeafIcon() {
  return (
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
      <path d="M11 20A7 7 0 014 13c0-3.87 3.13-7 7-7s7 3.13 7 7a7 7 0 01-7 7z" />
      <path d="M11 20c0-4.97 4-9 9-9" />
    </svg>
  );
}

function SearchIcon({ size = 20, color = "currentColor" }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="11" cy="11" r="8" />
      <line x1="21" y1="21" x2="16.65" y2="16.65" />
    </svg>
  );
}

function ScanIcon({ size = 20, color = "currentColor" }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
      <path d="M3 7V5a2 2 0 012-2h2M17 3h2a2 2 0 012 2v2M21 17v2a2 2 0 01-2 2h-2M7 21H5a2 2 0 01-2-2v-2" />
      <line x1="3" y1="12" x2="21" y2="12" />
    </svg>
  );
}

function HomeIcon({ size = 20, color = "currentColor" }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
      <path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z" />
      <polyline points="9 22 9 12 15 12 15 22" />
    </svg>
  );
}

function AnalyticsIcon({ size = 20, color = "currentColor" }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
      <line x1="18" y1="20" x2="18" y2="10" />
      <line x1="12" y1="20" x2="12" y2="4" />
      <line x1="6" y1="20" x2="6" y2="14" />
    </svg>
  );
}

function AboutIcon({ size = 20, color = "currentColor" }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="10" />
      <line x1="12" y1="16" x2="12" y2="12" />
      <line x1="12" y1="8" x2="12.01" y2="8" />
    </svg>
  );
}

function ProductCard({ p, isActive, offset, onClick }) {
  const absOff = Math.abs(offset);
  const x = offset * 170;
  const scale = isActive ? 1 : 0.88 - absOff * 0.04;
  const z = 10 - absOff;
  const opacity = isActive ? 1 : 0.55 - absOff * 0.1;
  const rotate = offset * 4;
  const rs = riskStyle(p.risk);

  return (
    <div
      onClick={onClick}
      style={{
        position: "absolute",
        width: 300,
        background: "#fff",
        borderRadius: 20,
        border: isActive ? `2px solid ${GREEN_MID}` : "1.5px solid #d4e8d4",
        padding: "28px 24px 24px",
        transform: `translateX(${x}px) scale(${scale}) rotate(${rotate}deg)`,
        zIndex: z,
        opacity,
        cursor: isActive ? "default" : "pointer",
        transition: "all 0.4s cubic-bezier(0.34,1.56,0.64,1)",
        boxShadow: isActive ? "0 16px 48px rgba(30,61,47,0.14)" : "0 2px 12px rgba(30,61,47,0.06)",
      }}
    >
      {/* Score circle */}
      <div style={{ display: "flex", flexDirection: "column", alignItems: "center", marginBottom: 18 }}>
        <div style={{ width: 64, height: 64, borderRadius: "50%", background: GREEN_MID, display: "flex", alignItems: "center", justifyContent: "center", marginBottom: 12 }}>
          <span style={{ color: "#fff", fontSize: 22, fontWeight: 600 }}>{p.waspas || p.composite}</span>
        </div>
        <div style={{ fontSize: 17, fontWeight: 600, color: "#0d3d22", marginBottom: 3, textAlign: "center", letterSpacing: "-0.2px" }}>{p.name}</div>
        <div style={{ fontSize: 13, color: GREEN_MUTED, marginBottom: 2, fontWeight: 500 }}>{p.brand}</div>
        {p.category && <div style={{ fontSize: 12, color: "#aacbaa", fontStyle: "italic" }}>{p.category}</div>}
      </div>

      {/* Score bars */}
      {Object.entries(p.scores).map(([key, val]) => (
        <div key={key} style={{ marginBottom: 10 }}>
          <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 3 }}>
            <span style={{ fontSize: 12, color: "#3a5a3a", fontWeight: 500 }}>{cap(key)}</span>
            <span style={{ fontSize: 12, fontWeight: 600, color: scoreColor(val) }}>{val}/100</span>
          </div>
          <div style={{ height: 5, background: "#e0ede0", borderRadius: 3 }}>
            <div style={{ height: 5, width: `${val}%`, background: scoreColor(val), borderRadius: 3, transition: "width 0.6s ease" }} />
          </div>
        </div>
      ))}

      {/* Bottom badges */}
      <div style={{ marginTop: 16, display: "flex", gap: 8, justifyContent: "center", flexWrap: "wrap" }}>
        <span style={{ fontSize: 11, fontWeight: 600, background: rs.bg, color: rs.color, padding: "4px 12px", borderRadius: 20 }}>
          {p.risk} Greenwashing Risk
        </span>
        {p.longevity && (
          <span style={{ fontSize: 11, fontWeight: 600, background: "#eef2ff", color: "#3a4a9a", padding: "4px 12px", borderRadius: 20 }}>
            Longevity: {typeof p.longevity === "object" ? p.longevity.label : p.longevity}
          </span>
        )}
      </div>

      {/* Greenwashing reason */}
      {p.greenwashing?.reason && (
        <div style={{ marginTop: 12, fontSize: 11, color: "#7a9a7a", textAlign: "center", lineHeight: 1.5, fontStyle: "italic" }}>
          {p.greenwashing.reason}
        </div>
      )}
    </div>
  );
}

function CardCarousel({ products }) {
  const [active, setActive] = useState(0);
  const total = products.length;
  const prev = () => setActive((a) => (a - 1 + total) % total);
  const next = () => setActive((a) => (a + 1) % total);

  return (
    <div style={{ position: "relative", width: "100%" }}>
      <button onClick={prev} style={{ position: "absolute", left: 0, top: "50%", transform: "translateY(-60%)", zIndex: 50, width: 44, height: 44, borderRadius: "50%", border: `1.5px solid ${GREEN_MID}`, background: "#fff", color: GREEN_MID, cursor: "pointer", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 20 }}>
        ‹
      </button>
      <button onClick={next} style={{ position: "absolute", right: 0, top: "50%", transform: "translateY(-60%)", zIndex: 50, width: 44, height: 44, borderRadius: "50%", border: `1.5px solid ${GREEN_MID}`, background: "#fff", color: GREEN_MID, cursor: "pointer", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 20 }}>
        ›
      </button>

      <div style={{ position: "relative", height: 540, display: "flex", alignItems: "center", justifyContent: "center" }}>
        {products.map((p, i) => {
          const offset = i - active;
          const absOff = Math.abs(offset);
          if (absOff > 2) return null;
          return (
            <ProductCard
              key={i}
              p={p}
              isActive={offset === 0}
              offset={offset}
              onClick={() => setActive(i)}
            />
          );
        })}
      </div>

      <div style={{ display: "flex", gap: 6, justifyContent: "center", marginTop: 8 }}>
        {products.map((_, i) => (
          <div key={i} onClick={() => setActive(i)} style={{ width: i === active ? 20 : 7, height: 7, borderRadius: 4, background: i === active ? GREEN_MID : "#c5dfc5", cursor: "pointer", transition: "all 0.3s ease" }} />
        ))}
      </div>
    </div>
  );
}

function HomePage() {
  return (
    <div style={{ padding: "40px 52px" }}>
      <div style={{ fontSize: 11, letterSpacing: "3px", textTransform: "uppercase", color: GREEN_MUTED, marginBottom: 16, fontWeight: 600 }}>Product Lookup</div>
      <h1 style={{ fontSize: 48, color: "#0d3d22", lineHeight: 1.1, fontWeight: 300, marginBottom: 16, letterSpacing: "-1px" }}>
        Know what's <em style={{ color: GREEN_ACCENT, fontStyle: "italic", fontWeight: 400 }}>really</em><br />in your basket
      </h1>
      <p style={{ fontSize: 16, color: "#5a7a6a", lineHeight: 1.8, maxWidth: 560, marginBottom: 48, fontWeight: 400 }}>
        Discover the truth behind everyday products with comprehensive sustainability, health, and transparency ratings — powered by verified data.
      </p>

      <div style={{ marginBottom: 24 }}>
        <h2 style={{ fontSize: 22, color: "#0d3d22", fontWeight: 600, marginBottom: 4, letterSpacing: "-0.3px" }}>Featured Products</h2>
        <p style={{ fontSize: 14, color: GREEN_MUTED, fontWeight: 400 }}>Browse our verified sustainable product catalogue</p>
      </div>

      <CardCarousel products={CATALOGUE_PRODUCTS} />

      <div style={{ background: "#fff", borderRadius: 16, padding: "28px 0", margin: "40px 0 0", display: "grid", gridTemplateColumns: "repeat(4,1fr)" }}>
        {DB_STATS.map((s, i) => (
          <div key={s.label} style={{ textAlign: "center", borderRight: i < 3 ? "1px solid #e5f0e5" : "none", padding: "0 20px" }}>
            <div style={{ fontSize: 34, color: GREEN_MID, fontWeight: 600, lineHeight: 1, letterSpacing: "-1px" }}>{s.val}</div>
            <div style={{ fontSize: 12, color: "#8abf9a", letterSpacing: "1px", textTransform: "uppercase", marginTop: 8, fontWeight: 500 }}>{s.label}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

function SearchPage() {
  const [barcode, setBarcode] = useState("");
  const [loading, setLoading] = useState(false);
  const [resultProducts, setResultProducts] = useState([]);
  const [error, setError] = useState("");
  const [weights, setWeights] = useState({ sustainability: 0.25, health: 0.25, transparency: 0.25, social: 0.25 });

  const updateWeight = (key, newVal) => {
    const val = parseFloat(newVal);
    const others = Object.keys(weights).filter((k) => k !== key);
    const otherTotal = others.reduce((s, k) => s + weights[k], 0);
    const remaining = 1 - val;
    const updated = { ...weights, [key]: val };
    if (otherTotal > 0) {
      others.forEach((k) => { updated[k] = parseFloat(((weights[k] / otherTotal) * remaining).toFixed(2)); });
    } else {
      others.forEach((k) => { updated[k] = parseFloat((remaining / 3).toFixed(2)); });
    }
    setWeights(updated);
  };

  const search = async () => {
    if (!barcode.trim()) return;
    setLoading(true); setError(""); setResultProducts([]);
    try {
      const w = weights;
      const res = await fetch(`http://127.0.0.1:8080/product/${barcode.trim()}?w1=${w.sustainability}&w2=${w.health}&w3=${w.transparency}&w4=${w.social}`);
      const data = await res.json();
      if (data.error) { setError("Product not found. Try another barcode."); setLoading(false); return; }

      // Format into card format
      const card = {
        name: data.name,
        brand: data.brand,
        category: "Scanned Product",
        scores: data.scores,
        waspas: data.composite,
        composite: data.composite,
        risk: data.greenwashing?.risk || "Unknown",
        longevity: data.longevity || null,
        greenwashing: data.greenwashing,
      };
      setResultProducts([card]);
    } catch { setError("Could not connect to server. Make sure your backend is running on port 8080."); }
    setLoading(false);
  };

  return (
    <div style={{ padding: "40px 52px" }}>
      <div style={{ fontSize: 11, letterSpacing: "3px", textTransform: "uppercase", color: GREEN_MUTED, marginBottom: 12, fontWeight: 600 }}>Barcode Search</div>
      <h2 style={{ fontSize: 30, color: "#0d3d22", fontWeight: 300, marginBottom: 8, letterSpacing: "-0.5px" }}>Search a product</h2>
      <p style={{ fontSize: 14, color: "#5a7a6a", marginBottom: 32, fontWeight: 400, lineHeight: 1.7 }}>Enter a barcode number to look up real-time sustainability, health, and transparency data.</p>

      {/* Search bar */}
      <div style={{ display: "flex", gap: 12, marginBottom: 32 }}>
        <div style={{ flex: 1, display: "flex", alignItems: "center", background: "#fff", border: `1.5px solid #c5dfc5`, borderRadius: 12, padding: "0 16px" }}>
          <SearchIcon size={18} color={GREEN_MUTED} />
          <input
            value={barcode}
            onChange={(e) => setBarcode(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && search()}
            placeholder="Enter barcode e.g. 8901719123894"
            style={{ flex: 1, padding: "14px 12px", border: "none", outline: "none", fontSize: 15, background: "transparent", color: "#0d3d22", fontFamily: "inherit" }}
          />
        </div>
        <button onClick={search} style={{ padding: "14px 28px", background: GREEN_MID, color: "#fff", border: "none", borderRadius: 12, fontSize: 14, fontWeight: 600, cursor: "pointer", letterSpacing: "0.3px" }}>
          Search
        </button>
      </div>

      {/* Priority sliders */}
      <div style={{ background: "#fff", borderRadius: 16, padding: 24, marginBottom: 32 }}>
        <div style={{ fontSize: 12, letterSpacing: "2px", textTransform: "uppercase", color: GREEN_MUTED, marginBottom: 16, fontWeight: 600 }}>Your Priorities</div>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20 }}>
          {Object.entries(weights).map(([key, val]) => (
            <div key={key}>
              <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 6 }}>
                <span style={{ fontSize: 13, color: "#0d3d22", fontWeight: 600 }}>{cap(key)}</span>
                <span style={{ fontSize: 13, fontWeight: 700, color: GREEN_MID }}>{Math.round(val * 100)}%</span>
              </div>
              <input type="range" min="0.05" max="0.85" step="0.01" value={val}
                onChange={(e) => updateWeight(key, e.target.value)}
                style={{ width: "100%", accentColor: GREEN_MID }} />
            </div>
          ))}
        </div>
        <p style={{ fontSize: 12, color: "#a0bfa8", marginTop: 12, fontWeight: 400 }}>
          Sliders auto-balance to always total 100%. Adjust to reflect what matters most to you.
        </p>
      </div>

      {loading && (
        <div style={{ textAlign: "center", color: GREEN_MUTED, padding: 40, fontSize: 15, fontWeight: 500 }}>
          Analysing product data…
        </div>
      )}
      {error && (
        <div style={{ background: "#fff0f0", color: "#b83232", padding: 16, borderRadius: 10, fontSize: 14, fontWeight: 500 }}>
          {error}
        </div>
      )}

      {resultProducts.length > 0 && (
        <div>
          <div style={{ marginBottom: 16 }}>
            <h3 style={{ fontSize: 18, color: "#0d3d22", fontWeight: 600, marginBottom: 4 }}>Result</h3>
            <p style={{ fontSize: 13, color: GREEN_MUTED, fontWeight: 400 }}>Swipe through the card to explore all scores</p>
          </div>
          <CardCarousel products={resultProducts} />
        </div>
      )}
    </div>
  );
}

function ScanPage({ onSwitchToSearch }) {
  const [scanning, setScanning] = useState(false);
  const [scannedCode, setScannedCode] = useState("");

  return (
    <div style={{ padding: "40px 52px" }}>
      <div style={{ fontSize: 11, letterSpacing: "3px", textTransform: "uppercase", color: GREEN_MUTED, marginBottom: 12, fontWeight: 600 }}>Barcode Scanner</div>
      <h2 style={{ fontSize: 30, color: "#0d3d22", fontWeight: 300, marginBottom: 8, letterSpacing: "-0.5px" }}>Scan a product</h2>
      <p style={{ fontSize: 14, color: "#5a7a6a", marginBottom: 40, fontWeight: 400, lineHeight: 1.7 }}>Use your device camera to instantly scan any product barcode and retrieve its sustainability profile.</p>

      {scannedCode && (
        <div style={{ background: GREEN_LIGHT, border: `1px solid ${GREEN_MID}`, borderRadius: 10, padding: 16, marginBottom: 24, fontSize: 14, color: "#0d3d22", fontWeight: 500 }}>
          Barcode Detected: <strong>{scannedCode}</strong> — Head to Search to look it up.
        </div>
      )}

      {!scanning ? (
        <div style={{ background: "#fff", borderRadius: 20, border: "1.5px solid #c5dfc5", padding: 48, textAlign: "center", maxWidth: 440, margin: "0 auto" }}>
          <div style={{ width: 160, height: 160, border: `2.5px solid ${GREEN_MID}`, borderRadius: 16, margin: "0 auto 32px", display: "flex", alignItems: "center", justifyContent: "center", position: "relative" }}>
            <div style={{ position: "absolute", top: -2, left: -2, width: 24, height: 24, borderTop: `3px solid ${GREEN_DARK}`, borderLeft: `3px solid ${GREEN_DARK}` }} />
            <div style={{ position: "absolute", top: -2, right: -2, width: 24, height: 24, borderTop: `3px solid ${GREEN_DARK}`, borderRight: `3px solid ${GREEN_DARK}` }} />
            <div style={{ position: "absolute", bottom: -2, left: -2, width: 24, height: 24, borderBottom: `3px solid ${GREEN_DARK}`, borderLeft: `3px solid ${GREEN_DARK}` }} />
            <div style={{ position: "absolute", bottom: -2, right: -2, width: 24, height: 24, borderBottom: `3px solid ${GREEN_DARK}`, borderRight: `3px solid ${GREEN_DARK}` }} />
            <ScanIcon size={48} color="#c5dfc5" />
          </div>
          <p style={{ fontSize: 15, color: "#5a7a6a", marginBottom: 8, fontWeight: 500 }}>Point your camera at any product barcode</p>
          <p style={{ fontSize: 13, color: GREEN_MUTED, marginBottom: 28, fontWeight: 400 }}>Supported on most modern browsers with camera access enabled.</p>
          <div style={{ display: "flex", gap: 12, justifyContent: "center" }}>
            <button onClick={() => setScanning(true)} style={{ padding: "12px 24px", background: GREEN_MID, color: "#fff", border: "none", borderRadius: 10, fontSize: 14, fontWeight: 600, cursor: "pointer" }}>
              Open Camera
            </button>
            <button onClick={onSwitchToSearch} style={{ padding: "12px 24px", background: "#fff", color: GREEN_MID, border: `1.5px solid ${GREEN_MID}`, borderRadius: 10, fontSize: 14, fontWeight: 500, cursor: "pointer" }}>
              Enter Manually
            </button>
          </div>
        </div>
      ) : (
        <div style={{ maxWidth: 440, margin: "0 auto" }}>
          <BarcodeScanner
            onScan={(code) => { setScannedCode(code); setScanning(false); }}
            onClose={() => setScanning(false)}
          />
        </div>
      )}
    </div>
  );
}

function AnalyticsPage() {
  const avgScores = ["sustainability", "health", "transparency", "social"].map((key) => ({
    label: key,
    avg: Math.round(CATALOGUE_PRODUCTS.reduce((s, p) => s + p.scores[key], 0) / CATALOGUE_PRODUCTS.length),
  }));
  const avgWaspas = Math.round(CATALOGUE_PRODUCTS.reduce((s, p) => s + p.waspas, 0) / CATALOGUE_PRODUCTS.length);
  const lowRisk = CATALOGUE_PRODUCTS.filter((p) => p.risk === "Low").length;

  return (
    <div style={{ padding: "40px 52px" }}>
      <div style={{ fontSize: 11, letterSpacing: "3px", textTransform: "uppercase", color: GREEN_MUTED, marginBottom: 12, fontWeight: 600 }}>Platform Insights</div>
      <h2 style={{ fontSize: 30, color: "#0d3d22", fontWeight: 300, marginBottom: 32, letterSpacing: "-0.5px" }}>Analytics Overview</h2>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(3,1fr)", gap: 16, marginBottom: 32 }}>
        {[
          { label: "Avg. WASPAS Score", val: avgWaspas, sub: "Across all catalogued products" },
          { label: "Products Catalogued", val: CATALOGUE_PRODUCTS.length, sub: "In current session" },
          { label: "Low Risk Products", val: lowRisk, sub: "Below greenwashing threshold" },
        ].map((c) => (
          <div key={c.label} style={{ background: "#fff", borderRadius: 14, padding: 24, border: "1px solid #e0ede0" }}>
            <div style={{ fontSize: 11, color: GREEN_MUTED, marginBottom: 8, textTransform: "uppercase", letterSpacing: "1px", fontWeight: 600 }}>{c.label}</div>
            <div style={{ fontSize: 38, color: GREEN_MID, lineHeight: 1, marginBottom: 6, fontWeight: 600, letterSpacing: "-1px" }}>{c.val}</div>
            <div style={{ fontSize: 13, color: "#a0bfa8", fontWeight: 400 }}>{c.sub}</div>
          </div>
        ))}
      </div>

      <div style={{ background: "#fff", borderRadius: 14, padding: 28, border: "1px solid #e0ede0", marginBottom: 24 }}>
        <div style={{ fontSize: 14, fontWeight: 600, color: "#0d3d22", marginBottom: 20 }}>Average Scores by Dimension</div>
        {avgScores.map((s) => (
          <div key={s.label} style={{ marginBottom: 16 }}>
            <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 6 }}>
              <span style={{ fontSize: 13, color: "#3a5a3a", fontWeight: 600 }}>{cap(s.label)}</span>
              <span style={{ fontSize: 13, fontWeight: 700, color: scoreColor(s.avg) }}>{s.avg}/100</span>
            </div>
            <div style={{ height: 10, background: "#e0ede0", borderRadius: 5 }}>
              <div style={{ height: 10, width: `${s.avg}%`, background: scoreColor(s.avg), borderRadius: 5 }} />
            </div>
          </div>
        ))}
      </div>

      <div style={{ background: "#fff", borderRadius: 14, padding: 28, border: "1px solid #e0ede0" }}>
        <div style={{ fontSize: 14, fontWeight: 600, color: "#0d3d22", marginBottom: 16 }}>Product Comparison</div>
        <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 13 }}>
          <thead>
            <tr style={{ borderBottom: "1.5px solid #e0ede0" }}>
              {["Product", "Brand", "WASPAS", "Risk"].map((h) => (
                <th key={h} style={{ textAlign: "left", padding: "8px 12px", color: GREEN_MUTED, fontWeight: 600, fontSize: 11, textTransform: "uppercase", letterSpacing: "1px" }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {CATALOGUE_PRODUCTS.map((p, i) => {
              const rs = riskStyle(p.risk);
              return (
                <tr key={i} style={{ borderBottom: "1px solid #f0f7f0" }}>
                  <td style={{ padding: "10px 12px", color: "#0d3d22", fontWeight: 500 }}>{p.name}</td>
                  <td style={{ padding: "10px 12px", color: GREEN_MUTED, fontWeight: 400 }}>{p.brand}</td>
                  <td style={{ padding: "10px 12px", color: GREEN_MID, fontWeight: 600 }}>{p.waspas}</td>
                  <td style={{ padding: "10px 12px" }}>
                    <span style={{ background: rs.bg, color: rs.color, padding: "3px 10px", borderRadius: 20, fontSize: 11, fontWeight: 600 }}>{p.risk}</span>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function AboutPage() {
  const pillars = [
    { title: "Sustainability", desc: "Environmental impact, carbon footprint, packaging and supply chain eco-scores sourced from Open Food Facts and verified eco-score databases." },
    { title: "Health & Safety", desc: "Nutritional data, additives and NutriScore ratings from verified food databases, mapped to a clear 0–100 health index." },
    { title: "Transparency", desc: "Ingredient completeness, label certification count and traceability scoring — rewarding brands that clearly show their workings." },
    { title: "Social Impact", desc: "Fair trade certification, ethical sourcing and manufacturing origin data aggregated from public brand disclosures and third-party audits." },
  ];

  return (
    <div style={{ padding: "40px 52px" }}>
      <div style={{ fontSize: 11, letterSpacing: "3px", textTransform: "uppercase", color: GREEN_MUTED, marginBottom: 12, fontWeight: 600 }}>About ClarityX</div>
      <h2 style={{ fontSize: 30, color: "#0d3d22", fontWeight: 300, marginBottom: 16, letterSpacing: "-0.5px" }}>The platform behind the scores</h2>
      <p style={{ fontSize: 15, color: "#5a7a6a", lineHeight: 1.8, maxWidth: 600, marginBottom: 48, fontWeight: 400 }}>
        ClarityX cross-references the Open Food Facts database — covering over 3 million products — with eco-score indexes, nutritional databases, and social responsibility disclosures to produce a single weighted composite score for any barcoded product.
      </p>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20, marginBottom: 40 }}>
        {pillars.map((p) => (
          <div key={p.title} style={{ background: "#fff", borderRadius: 14, padding: 24, border: "1px solid #e0ede0" }}>
            <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 12 }}>
              <div style={{ width: 8, height: 8, borderRadius: "50%", background: GREEN_MID, flexShrink: 0 }} />
              <span style={{ fontSize: 15, fontWeight: 600, color: "#0d3d22" }}>{p.title}</span>
            </div>
            <p style={{ fontSize: 13, color: "#5a7a6a", lineHeight: 1.7, fontWeight: 400 }}>{p.desc}</p>
          </div>
        ))}
      </div>

      <div style={{ background: GREEN_DARK, borderRadius: 16, padding: 32, color: "#fff" }}>
        <div style={{ fontSize: 18, fontWeight: 600, marginBottom: 12, letterSpacing: "-0.3px" }}>WASPAS Scoring Method</div>
        <p style={{ fontSize: 14, color: "rgba(255,255,255,0.8)", lineHeight: 1.8, fontWeight: 400 }}>
          The Weighted Aggregated Sum Product Assessment (WASPAS) combines a Weighted Sum Model (WSM) and a Weighted Product Model (WPM) with equal weighting (λ = 0.5). This hybrid approach is more reliable than either method alone, balancing additive and multiplicative relationships between sustainability criteria.
        </p>
      </div>
    </div>
  );
}

const SIDEBAR_ITEMS = [
  { id: "home", label: "Home", Icon: HomeIcon },
  { id: "search", label: "Search", Icon: SearchIcon },
  { id: "scan", label: "Scan", Icon: ScanIcon },
  { id: "analytics", label: "Analytics", Icon: AnalyticsIcon },
  { id: "about", label: "About", Icon: AboutIcon },
];

function Sidebar({ active, onNavigate }) {
  return (
    <div style={{ width: 72, background: GREEN_DARK, display: "flex", flexDirection: "column", alignItems: "center", padding: "20px 0", flexShrink: 0, minHeight: "100vh" }}>
      <div style={{ width: 42, height: 42, background: GREEN_MID, borderRadius: 12, display: "flex", alignItems: "center", justifyContent: "center", marginBottom: 32 }}>
        <LeafIcon />
      </div>
      <div style={{ display: "flex", flexDirection: "column", gap: 4, width: "100%", alignItems: "center" }}>
        {SIDEBAR_ITEMS.map(({ id, label, Icon }) => {
          const isActive = active === id;
          return (
            <button key={id} onClick={() => onNavigate(id)} style={{ width: 56, display: "flex", flexDirection: "column", alignItems: "center", gap: 5, padding: "10px 0", borderRadius: 12, border: "none", background: isActive ? "rgba(255,255,255,0.15)" : "transparent", color: isActive ? "#fff" : "rgba(255,255,255,0.45)", cursor: "pointer", transition: "all 0.2s" }}>
              <Icon size={20} color={isActive ? "#fff" : "rgba(255,255,255,0.45)"} />
              <span style={{ fontSize: 9, letterSpacing: "0.5px", textTransform: "uppercase", fontWeight: 600 }}>{label}</span>
            </button>
          );
        })}
      </div>
    </div>
  );
}

export default function App() {
  const [page, setPage] = useState("home");

  const pages = {
    home: <HomePage />,
    search: <SearchPage />,
    scan: <ScanPage onSwitchToSearch={() => setPage("search")} />,
    analytics: <AnalyticsPage />,
    about: <AboutPage />,
  };

  return (
    <div style={{ display: "flex", minHeight: "100vh", background: BG, fontFamily: "'Segoe UI', system-ui, -apple-system, sans-serif" }}>
      <Sidebar active={page} onNavigate={setPage} />
      <main style={{ flex: 1, overflowY: "auto", minHeight: "100vh" }}>
        {pages[page]}
      </main>
    </div>
  );
}