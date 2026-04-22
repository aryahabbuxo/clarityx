import { useEffect, useRef } from "react";
import { BrowserMultiFormatReader } from "@zxing/library";

function BarcodeScanner({ onScan, onClose }) {
  const videoRef = useRef();

  useEffect(() => {
    const reader = new BrowserMultiFormatReader();
    reader.decodeFromVideoDevice(null, videoRef.current, (result, err) => {
      if (result) {
        onScan(result.getText());
        reader.reset();
      }
    });
    return () => reader.reset();
  }, [onScan]);

  return (
    <div style={{ marginBottom: 16 }}>
      <video ref={videoRef} style={{ width: "100%", borderRadius: 8 }} />
      <button
        onClick={onClose}
        style={{ marginTop: 8, padding: "8px 16px", background: "#d9534f", color: "white", border: "none", borderRadius: 8, cursor: "pointer" }}
      >
        Cancel
      </button>
    </div>
  );
}

export default BarcodeScanner;