import { useEffect, useState } from "react";
import BarcodeScanner from "./BarcodeScanner";

const GREEN_DARK = "#1e3d2f";
const GREEN_MID = "#2d6a4f";
const GREEN_ACCENT = "#3a8a5a";
const GREEN_LIGHT = "#e8f5e0";
const GREEN_MUTED = "#6aaa7e";
const BG = "#f5f6f0";
const STORAGE_KEY = "clarityx-lookups";
const LEGACY_STORAGE_KEYS = ["clarityx-products", "clarityx-scans", "clarityx-product-data"];
const PRODUCT_SCHEMA_VERSION = 3;
const SCORE_KEYS = [
  "regulatory_compliance",
  "ingredient_safety",
  "nutritional_quality",
  "certification_credibility",
  "heritage_authenticity",
  "transparency",
  "traceability_confidence",
];
const SCORE_DETAIL_KEY_MAP = {
  RegulatoryComplianceScore: "regulatory_compliance",
  IngredientSafetyScore: "ingredient_safety",
  NutritionalQualityScore: "nutritional_quality",
  CertificationCredibilityScore: "certification_credibility",
  HeritageAuthenticityScore: "heritage_authenticity",
  TransparencyScore: "transparency",
  TraceabilityConfidenceScore: "traceability_confidence",
};

function isFiniteScore(value) {
  return typeof value === "number" && Number.isFinite(value);
}

function hasCompleteEvidenceScores(scores) {
  return Boolean(scores) && SCORE_KEYS.every((key) => isFiniteScore(scores[key]));
}

function isCompleteProductScore(product) {
  return Boolean(product) && isFiniteScore(product.waspas) && hasCompleteEvidenceScores(product.scores);
}

function scoreLabel(value) {
  return isFiniteScore(value) ? `${Math.round(value)}/100` : "No Data";
}

function scoreWidth(value) {
  return isFiniteScore(value) ? `${Math.max(0, Math.min(100, value))}%` : "0%";
}

function scoreDisplayColor(value) {
  return isFiniteScore(value) ? scoreColor(value) : GREEN_MUTED;
}

function normalizeScores(scores, scoreDetails) {
  const normalized = {};

  SCORE_KEYS.forEach((key) => {
    if (isFiniteScore(scores?.[key])) normalized[key] = scores[key];
  });

  Object.entries(SCORE_DETAIL_KEY_MAP).forEach(([detailKey, scoreKey]) => {
    const detailScore = scoreDetails?.[detailKey]?.score;
    if (!isFiniteScore(normalized[scoreKey]) && isFiniteScore(detailScore)) {
      normalized[scoreKey] = detailScore;
    }
  });

  return normalized;
}

function productFromApi(data, barcode) {
  const scores = normalizeScores(data.scores, data.score_details);
  const compositeScore = isFiniteScore(data.score) ? data.score : null;

  return {
    schema_version: PRODUCT_SCHEMA_VERSION,
    score_schema_version: data.score_schema_version || null,
    barcode,
    name: data.name,
    brand: data.brand,
    category: data.identity?.category || "Scanned Product",
    scores,
    score_details: data.score_details,
    evidence_graph: data.evidence_graph,
    confidence: data.confidence,
    waspas: compositeScore,
    composite: compositeScore,
    risk: data.greenwashing?.risk || "Unknown",
    longevity: data.longevity || null,
    greenwashing: data.greenwashing,
    heritageFacts: data.heritage_facts || [],
    dataSources: data.data_sources,
  };
}

function migrateProduct(product) {
  if (!product || typeof product !== "object") return null;

  const scores = normalizeScores(product.scores, product.score_details);
  const compositeScore = isFiniteScore(product.waspas)
    ? product.waspas
    : isFiniteScore(product.composite)
      ? product.composite
      : isFiniteScore(product.score)
        ? product.score
        : null;

  const migrated = {
    ...product,
    schema_version: PRODUCT_SCHEMA_VERSION,
    scores,
    waspas: compositeScore,
    composite: compositeScore,
    heritageFacts: Array.isArray(product.heritageFacts) ? product.heritageFacts : [],
  };

  return isCompleteProductScore(migrated) ? migrated : null;
}

function parseStoredProducts(raw) {
  if (!raw) return [];

  try {
    const parsed = JSON.parse(raw);
    const records = Array.isArray(parsed) ? parsed : parsed?.products;
    if (!Array.isArray(records)) return [];
    return records.map(migrateProduct).filter(Boolean).slice(0, 12);
  } catch {
    return [];
  }
}

function loadStoredProducts() {
  LEGACY_STORAGE_KEYS.forEach((key) => localStorage.removeItem(key));
  const products = parseStoredProducts(localStorage.getItem(STORAGE_KEY));
  localStorage.setItem(
    STORAGE_KEY,
    JSON.stringify({ schema_version: PRODUCT_SCHEMA_VERSION, products })
  );
  return products;
}

function persistProducts(products) {
  const storedProducts = products.map(migrateProduct).filter(Boolean).slice(0, 12);
  localStorage.setItem(
    STORAGE_KEY,
    JSON.stringify({ schema_version: PRODUCT_SCHEMA_VERSION, products: storedProducts })
  );
}

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
  return str.split("_").map((part) => part.charAt(0).toUpperCase() + part.slice(1)).join(" ");
}

function formatDataSources(dataSources) {
  if (!dataSources) return "";
  if (typeof dataSources === "string") return dataSources;
  if (Array.isArray(dataSources)) return dataSources.join(", ");
  return Object.entries(dataSources)
    .map(([key, value]) => `${cap(key)}: ${Array.isArray(value) ? value.join(", ") : value}`)
    .join(" | ");
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
  const scoreValue = isFiniteScore(p.waspas) ? p.waspas : p.composite;
  const dataSourceText = formatDataSources(p.dataSources);

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
          <span style={{ color: "#fff", fontSize: isFiniteScore(scoreValue) ? 22 : 12, fontWeight: 600 }}>{isFiniteScore(scoreValue) ? Math.round(scoreValue) : "No Data"}</span>
        </div>
        <div style={{ fontSize: 17, fontWeight: 600, color: "#0d3d22", marginBottom: 3, textAlign: "center", letterSpacing: "-0.2px" }}>{p.name}</div>
        <div style={{ fontSize: 13, color: GREEN_MUTED, marginBottom: 2, fontWeight: 500 }}>{p.brand}</div>
        {p.category && <div style={{ fontSize: 12, color: "#aacbaa", fontStyle: "italic" }}>{p.category}</div>}
      </div>

      {/* Score bars */}
      {SCORE_KEYS.map((key) => {
        const val = p.scores?.[key];
        return (
        <div key={key} style={{ marginBottom: 10 }}>
          <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 3 }}>
            <span style={{ fontSize: 12, color: "#3a5a3a", fontWeight: 500 }}>{cap(key)}</span>
            <span style={{ fontSize: 12, fontWeight: 600, color: scoreDisplayColor(val) }}>{scoreLabel(val)}</span>
          </div>
          <div style={{ height: 5, background: "#e0ede0", borderRadius: 3 }}>
            <div style={{ height: 5, width: scoreWidth(val), background: scoreDisplayColor(val), borderRadius: 3, transition: "width 0.6s ease" }} />
          </div>
        </div>
        );
      })}

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

      {p.heritageFacts?.[0] && (
        <div role="status" style={{ marginTop: 16, background: "#f2f8e9", border: "1px solid #cfe3b5", borderRadius: 12, padding: "12px 13px", color: "#31562d" }}>
          <div style={{ fontSize: 11, fontWeight: 700, letterSpacing: "0.7px", textTransform: "uppercase", marginBottom: 5 }}>Heritage fun fact</div>
          <div style={{ fontSize: 12, lineHeight: 1.5 }}>{p.heritageFacts[0].fun_fact}</div>
          <div style={{ fontSize: 10, lineHeight: 1.35, marginTop: 7, color: "#668363" }}>{p.heritageFacts[0].disclaimer}</div>
        </div>
      )}

      {dataSourceText && (
        <div style={{ marginTop: 10, fontSize: 10, color: "#8aa48f", textAlign: "center" }}>Data: {dataSourceText}</div>
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

function HomePage({ products }) {
  const scans = products.length;
  const scoredProducts = products.filter(isCompleteProductScore);
  const averageScore = scoredProducts.length ? Math.round(scoredProducts.reduce((sum, p) => sum + p.waspas, 0) / scoredProducts.length) : null;
  const heritageMatches = products.reduce((sum, p) => sum + (p.heritageFacts?.length || 0), 0);
  const lowRisk = products.filter((p) => p.risk === "Low").length;
  return (
    <div style={{ padding: "40px 52px" }}>
      <div style={{ fontSize: 11, letterSpacing: "3px", textTransform: "uppercase", color: GREEN_MUTED, marginBottom: 16, fontWeight: 600 }}>Product Lookup</div>
      <h1 style={{ fontSize: 48, color: "#0d3d22", lineHeight: 1.1, fontWeight: 300, marginBottom: 16, letterSpacing: "-1px" }}>
        Know what's <em style={{ color: GREEN_ACCENT, fontStyle: "italic", fontWeight: 400 }}>really</em><br />in your basket
      </h1>
      <p style={{ fontSize: 16, color: "#5a7a6a", lineHeight: 1.8, maxWidth: 560, marginBottom: 48, fontWeight: 400 }}>
        Identify products from barcode databases, then score ingredients from regulator and standards evidence.
      </p>

      <div style={{ marginBottom: 24 }}>
        <h2 style={{ fontSize: 22, color: "#0d3d22", fontWeight: 600, marginBottom: 4, letterSpacing: "-0.3px" }}>Your recent lookups</h2>
        <p style={{ fontSize: 14, color: GREEN_MUTED, fontWeight: 400 }}>Saved in this browser, so your dashboard reflects real scans instead of sample products.</p>
      </div>

      {scans ? <CardCarousel products={products} /> : (
        <div style={{ background: "#fff", border: "1.5px dashed #c5dfc5", borderRadius: 16, padding: "44px 28px", textAlign: "center", color: GREEN_MUTED }}>
          Your first verified lookup will appear here.
        </div>
      )}

      <div style={{ background: "#fff", borderRadius: 16, padding: "28px 0", margin: "40px 0 0", display: "grid", gridTemplateColumns: "repeat(4,1fr)" }}>
        {[
          { val: scans, label: "Lookups saved" },
          { val: averageScore === null ? "—" : `${averageScore}/100`, label: "Average score" },
          { val: heritageMatches, label: "Heritage matches" },
          { val: lowRisk, label: "Low-risk products" },
        ].map((s, i) => (
          <div key={s.label} style={{ textAlign: "center", borderRight: i < 3 ? "1px solid #e5f0e5" : "none", padding: "0 20px" }}>
            <div style={{ fontSize: 34, color: GREEN_MID, fontWeight: 600, lineHeight: 1, letterSpacing: "-1px" }}>{s.val}</div>
            <div style={{ fontSize: 12, color: "#8abf9a", letterSpacing: "1px", textTransform: "uppercase", marginTop: 8, fontWeight: 500 }}>{s.label}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

function SearchPage({ onProductLookup }) {
  const [barcode, setBarcode] = useState("");
  const [loading, setLoading] = useState(false);
  const [resultProducts, setResultProducts] = useState([]);
  const [error, setError] = useState("");

  const search = async () => {
    if (!barcode.trim()) return;
    setLoading(true); setError(""); setResultProducts([]);
    try {
      const res = await fetch(`http://127.0.0.1:8080/product/${barcode.trim()}`);
      const data = await res.json();
      if (data.error) { setError("Product not found. Try another barcode."); setLoading(false); return; }

      const card = productFromApi(data, barcode.trim());
      setResultProducts([card]);
      onProductLookup(card);
    } catch { setError("Could not connect to server. Make sure your backend is running on port 8080."); }
    setLoading(false);
  };

  return (
    <div style={{ padding: "40px 52px" }}>
      <div style={{ fontSize: 11, letterSpacing: "3px", textTransform: "uppercase", color: GREEN_MUTED, marginBottom: 12, fontWeight: 600 }}>Barcode Search</div>
      <h2 style={{ fontSize: 30, color: "#0d3d22", fontWeight: 300, marginBottom: 8, letterSpacing: "-0.5px" }}>Search a product</h2>
      <p style={{ fontSize: 14, color: "#5a7a6a", marginBottom: 32, fontWeight: 400, lineHeight: 1.7 }}>Enter a barcode number to look up product identity and regulator-backed ingredient evidence.</p>

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

function ScanPage({ onSwitchToSearch, onProductLookup }) {
  const [scanning, setScanning]     = useState(false);
  const [scannedCode, setScannedCode] = useState("");
  const [loading, setLoading]       = useState(false);
  const [result, setResult]         = useState(null);
  const [error, setError]           = useState("");
 
  // Called automatically the moment the camera reads a barcode.
  // Closes the camera, saves the code, and fires the API call immediately.
  const handleScan = async (code) => {
    setScanning(false);
    setScannedCode(code);
    setResult(null);
    setError("");
    setLoading(true);
 
    try {
      const res = await fetch(
        `http://127.0.0.1:8080/product/${code}`
      );
      const data = await res.json();
 
      if (data.error) {
        setError("Product not found in any database.");
      } else {
        const card = productFromApi(data, code);
        setResult(card);
        onProductLookup(card);
      }
    } catch {
      setError("Could not connect to backend. Make sure it's running on port 8080.");
    }
 
    setLoading(false);
  };
 
  const resetScan = () => {
    setScanning(true);
    setScannedCode("");
    setResult(null);
    setError("");
  };
 
  return (
    <div style={{ padding: "40px 52px" }}>
      {/* Page header */}
      <div style={{ fontSize: 11, letterSpacing: "3px", textTransform: "uppercase", color: GREEN_MUTED, marginBottom: 12, fontWeight: 600 }}>
        Barcode Scanner
      </div>
      <h2 style={{ fontSize: 30, color: "#0d3d22", fontWeight: 300, marginBottom: 8, letterSpacing: "-0.5px" }}>
        Scan a product
      </h2>
      <p style={{ fontSize: 14, color: "#5a7a6a", marginBottom: 40, fontWeight: 400, lineHeight: 1.7 }}>
        Use your device camera to identify a product and retrieve regulator-backed ingredient evidence.
      </p>
 
      {/* Detected barcode banner — shown as soon as a code is read */}
      {scannedCode && (
        <div style={{ background: GREEN_LIGHT, border: `1px solid ${GREEN_MID}`, borderRadius: 10, padding: 16, marginBottom: 24, fontSize: 14, color: "#0d3d22", fontWeight: 500 }}>
          Barcode detected: <strong>{scannedCode}</strong>
          {loading && <span style={{ color: GREEN_MUTED, fontWeight: 400 }}> — Fetching product data…</span>}
        </div>
      )}
 
      {/* Camera feed (active) or idle placeholder */}
      {scanning ? (
        <div style={{ maxWidth: 440, margin: "0 auto" }}>
          {/* BarcodeScanner calls onScan(code) automatically; no button press needed */}
          <BarcodeScanner
            onScan={handleScan}
            onClose={() => setScanning(false)}
          />
        </div>
      ) : (
        <div style={{ background: "#fff", borderRadius: 20, border: "1.5px solid #c5dfc5", padding: 48, textAlign: "center", maxWidth: 440, margin: "0 auto" }}>
          {/* Viewfinder graphic */}
          <div style={{ width: 160, height: 160, border: `2.5px solid ${GREEN_MID}`, borderRadius: 16, margin: "0 auto 32px", display: "flex", alignItems: "center", justifyContent: "center", position: "relative" }}>
            <div style={{ position: "absolute", top: -2, left: -2,  width: 24, height: 24, borderTop:    `3px solid ${GREEN_DARK}`, borderLeft:  `3px solid ${GREEN_DARK}` }} />
            <div style={{ position: "absolute", top: -2, right: -2, width: 24, height: 24, borderTop:    `3px solid ${GREEN_DARK}`, borderRight: `3px solid ${GREEN_DARK}` }} />
            <div style={{ position: "absolute", bottom: -2, left: -2,  width: 24, height: 24, borderBottom: `3px solid ${GREEN_DARK}`, borderLeft:  `3px solid ${GREEN_DARK}` }} />
            <div style={{ position: "absolute", bottom: -2, right: -2, width: 24, height: 24, borderBottom: `3px solid ${GREEN_DARK}`, borderRight: `3px solid ${GREEN_DARK}` }} />
            <ScanIcon size={48} color="#c5dfc5" />
          </div>
 
          <p style={{ fontSize: 15, color: "#5a7a6a", marginBottom: 8, fontWeight: 500 }}>
            Point your camera at any product barcode
          </p>
          <p style={{ fontSize: 13, color: GREEN_MUTED, marginBottom: 28, fontWeight: 400 }}>
            Results appear automatically — no button press needed.
          </p>
 
          <div style={{ display: "flex", gap: 12, justifyContent: "center" }}>
            <button
              onClick={resetScan}
              style={{ padding: "12px 24px", background: GREEN_MID, color: "#fff", border: "none", borderRadius: 10, fontSize: 14, fontWeight: 600, cursor: "pointer" }}
            >
              {scannedCode ? "Scan Again" : "Open Camera"}
            </button>
            <button
              onClick={onSwitchToSearch}
              style={{ padding: "12px 24px", background: "#fff", color: GREEN_MID, border: `1.5px solid ${GREEN_MID}`, borderRadius: 10, fontSize: 14, fontWeight: 500, cursor: "pointer" }}
            >
              Enter Manually
            </button>
          </div>
        </div>
      )}
 
      {/* Loading indicator */}
      {loading && (
        <div style={{ textAlign: "center", color: GREEN_MUTED, padding: 40, fontSize: 15, fontWeight: 500 }}>
          Analysing product data…
        </div>
      )}
 
      {/* Error state */}
      {error && (
        <div style={{ background: "#fff0f0", color: "#b83232", padding: 16, borderRadius: 10, fontSize: 14, fontWeight: 500, marginTop: 24 }}>
          {error}
        </div>
      )}
 
      {/* Result card — reuses the exact same CardCarousel + ProductCard as SearchPage */}
      {result && !loading && (
        <div style={{ marginTop: 32 }}>
          <h3 style={{ fontSize: 18, color: "#0d3d22", fontWeight: 600, marginBottom: 4 }}>Result</h3>
          <p style={{ fontSize: 13, color: GREEN_MUTED, fontWeight: 400, marginBottom: 16 }}>
            Scanned product analysis
          </p>
          <CardCarousel products={[result]} />
        </div>
      )}
    </div>
  );
}

function AnalyticsPage({ products }) {
  const analyticsProducts = products.filter(isCompleteProductScore);
  const hasProducts = analyticsProducts.length > 0;
  const avgScores = SCORE_KEYS.map((key) => ({
    label: key,
    avg: hasProducts ? Math.round(analyticsProducts.reduce((s, p) => s + p.scores[key], 0) / analyticsProducts.length) : null,
  }));
  const avgWaspas = hasProducts ? Math.round(analyticsProducts.reduce((s, p) => s + p.waspas, 0) / analyticsProducts.length) : null;
  const lowRisk = analyticsProducts.filter((p) => p.risk === "Low").length;

  return (
    <div style={{ padding: "40px 52px" }}>
      <div style={{ fontSize: 11, letterSpacing: "3px", textTransform: "uppercase", color: GREEN_MUTED, marginBottom: 12, fontWeight: 600 }}>Platform Insights</div>
      <h2 style={{ fontSize: 30, color: "#0d3d22", fontWeight: 300, marginBottom: 32, letterSpacing: "-0.5px" }}>Analytics Overview</h2>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(3,1fr)", gap: 16, marginBottom: 32 }}>
        {[
          { label: "Avg. Evidence Score", val: scoreLabel(avgWaspas), sub: "Across complete evidence lookups" },
          { label: "Products Analysed", val: analyticsProducts.length, sub: "Complete saved evidence records" },
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
        {!hasProducts && <p style={{ fontSize: 14, color: GREEN_MUTED, marginBottom: 20 }}>No complete evidence-engine score records yet. Scan or search a barcode to build your personal analytics.</p>}
        {avgScores.map((s) => (
          <div key={s.label} style={{ marginBottom: 16 }}>
            <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 6 }}>
              <span style={{ fontSize: 13, color: "#3a5a3a", fontWeight: 600 }}>{cap(s.label)}</span>
              <span style={{ fontSize: 13, fontWeight: 700, color: scoreDisplayColor(s.avg) }}>{scoreLabel(s.avg)}</span>
            </div>
            <div style={{ height: 10, background: "#e0ede0", borderRadius: 5 }}>
              <div style={{ height: 10, width: scoreWidth(s.avg), background: scoreDisplayColor(s.avg), borderRadius: 5 }} />
            </div>
          </div>
        ))}
      </div>

      <div style={{ background: "#fff", borderRadius: 14, padding: 28, border: "1px solid #e0ede0" }}>
        <div style={{ fontSize: 14, fontWeight: 600, color: "#0d3d22", marginBottom: 16 }}>Product Comparison</div>
        <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 13 }}>
          <thead>
            <tr style={{ borderBottom: "1.5px solid #e0ede0" }}>
              {["Product", "Brand", "Score", "Risk"].map((h) => (
                <th key={h} style={{ textAlign: "left", padding: "8px 12px", color: GREEN_MUTED, fontWeight: 600, fontSize: 11, textTransform: "uppercase", letterSpacing: "1px" }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {analyticsProducts.map((p, i) => {
              const rs = riskStyle(p.risk);
              return (
                <tr key={i} style={{ borderBottom: "1px solid #f0f7f0" }}>
                  <td style={{ padding: "10px 12px", color: "#0d3d22", fontWeight: 500 }}>{p.name}</td>
                  <td style={{ padding: "10px 12px", color: GREEN_MUTED, fontWeight: 400 }}>{p.brand}</td>
                  <td style={{ padding: "10px 12px", color: GREEN_MID, fontWeight: 600 }}>{scoreLabel(p.waspas)}</td>
                  <td style={{ padding: "10px 12px" }}>
                    <span style={{ background: rs.bg, color: rs.color, padding: "3px 10px", borderRadius: 20, fontSize: 11, fontWeight: 600 }}>{p.risk}</span>
                  </td>
                </tr>
              );
            })}
            {!hasProducts && <tr><td colSpan="4" style={{ padding: "18px 12px", color: GREEN_MUTED }}>No products analysed yet.</td></tr>}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function AboutPage() {
  const pillars = [
    { title: "Product Identity", desc: "Open Food Facts and Open Beauty Facts identify the product, manufacturer, category, and ingredient text only." },
    { title: "Regulatory Evidence", desc: "EFSA, FDA, Codex, FSSAI, REACH, CDSCO, AYUSH, NIN, and GS1 evidence records evaluate ingredients and traceability." },
    { title: "Evidence Graph", desc: "Every score contribution is stored as an ingredient, source, regulation, confidence, and contribution chain." },
    { title: "Confidence", desc: "Missing evidence reduces confidence without automatically treating unknown ingredients as unsafe." },
  ];

  return (
    <div style={{ padding: "40px 52px" }}>
      <div style={{ fontSize: 11, letterSpacing: "3px", textTransform: "uppercase", color: GREEN_MUTED, marginBottom: 12, fontWeight: 600 }}>About ClarityX</div>
      <h2 style={{ fontSize: 30, color: "#0d3d22", fontWeight: 300, marginBottom: 16, letterSpacing: "-0.5px" }}>The platform behind the scores</h2>
      <p style={{ fontSize: 15, color: "#5a7a6a", lineHeight: 1.8, maxWidth: 600, marginBottom: 48, fontWeight: 400 }}>
        ClarityX uses identity databases to identify products and regulator-backed evidence to evaluate ingredients. Scores are generated from auditable evidence graph records, not brand reputation or packaging claims.
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
        <div style={{ fontSize: 18, fontWeight: 600, marginBottom: 12, letterSpacing: "-0.3px" }}>Evidence Scoring Method</div>
        <p style={{ fontSize: 14, color: "rgba(255,255,255,0.8)", lineHeight: 1.8, fontWeight: 400 }}>
          Each score consumes only evidence graph data. Unknown provider results are preserved as UNKNOWN and affect confidence, not automatic safety conclusions.
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
  const [products, setProducts] = useState(loadStoredProducts);

  useEffect(() => {
    persistProducts(products);
  }, [products]);

  const recordProduct = (product) => {
    const normalized = migrateProduct(product);
    if (!normalized) return;
    setProducts((current) => [normalized, ...current.filter((item) => item.barcode !== normalized.barcode)].slice(0, 12));
  };

  const pages = {
    home: <HomePage products={products} />,
    search: <SearchPage onProductLookup={recordProduct} />,
    scan: <ScanPage onSwitchToSearch={() => setPage("search")} onProductLookup={recordProduct} />,
    analytics: <AnalyticsPage products={products} />,
    about: <AboutPage />,
  };

  return (
    <div style={{ display: "flex", minHeight: "100vh", background: BG, fontFamily: "'Segoe UI', system-ui, -apple-system, sans-serif" }}>
      <Sidebar active={page} onNavigate={setPage} />
      <main style={{ flex: 1, overflowY: "auto", minHeight: "100vh" }}>
        {pages[page]}
        <footer style={{ padding: "24px 52px 32px", color: "#668363", fontSize: 12, lineHeight: 1.6 }}>
          <strong style={{ color: "#31562d" }}>How ClarityX works:</strong> Open Food Facts and Open Beauty Facts identify products only. Regulatory and standards providers evaluate ingredients, persist evidence graph records, and produce auditable scores. Heritage notes describe identity and references only, not efficacy or medical claims.
        </footer>
      </main>
    </div>
  );
}
