import React, { useState } from "react";
import axios from "axios";
import SectionList from "./components/SectionList";
import JsonViewer from "./components/JsonViewer";

const App = () => {
  const [url, setUrl] = useState("");
  const [mode, setMode] = useState("auto");
  const [deep, setDeep] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);
  const [showRawJson, setShowRawJson] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!url) return;
    setError("");
    setLoading(true);
    setResult(null);

    try {
      const res = await axios.post("/scrape", {
        url,
        mode,
        deep,
      });
      setResult(res.data.result);
    } catch (err) {
      console.error(err);
      setError(
        err.response?.data?.detail ||
          "Failed to scrape URL. Check server logs for details."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = () => {
    if (!result) return;
    const blob = new Blob([JSON.stringify({ result }, null, 2)], {
      type: "application/json",
    });
    const href = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = href;
    a.download = "scrape-result.json";
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(href);
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        background: "#020617",
        color: "#e5e7eb",
        fontFamily: "system-ui, -apple-system, BlinkMacSystemFont, sans-serif",
      }}
    >
      <div style={{ maxWidth: 1080, margin: "0 auto", padding: "1.5rem" }}>
        <header style={{ marginBottom: "1.5rem" }}>
          <h1 style={{ fontSize: "1.9rem", marginBottom: "0.3rem" }}>
            Universal Website Scraper
          </h1>
          <p style={{ color: "#9ca3af", fontSize: "0.95rem" }}>
            Static-first scraping with JS fallback, interaction tracing, and a
            simple JSON viewer.
          </p>
        </header>

        <section
          style={{
            marginBottom: "1rem",
            padding: "1rem",
            borderRadius: "0.75rem",
            background:
              "radial-gradient(circle at top left, #1d4ed8 0, #020617 55%)",
            border: "1px solid #1f2937",
          }}
        >
          <form
            onSubmit={handleSubmit}
            style={{
              display: "flex",
              flexDirection: "column",
              gap: "0.75rem",
            }}
          >
            <div style={{ display: "flex", gap: "0.5rem" }}>
              <input
                type="url"
                placeholder="https://example.com"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                style={{
                  flex: 1,
                  padding: "0.6rem 0.75rem",
                  borderRadius: "0.5rem",
                  border: "1px solid #1f2937",
                  background: "#020617",
                  color: "#e5e7eb",
                  fontSize: "0.9rem",
                }}
                required
              />
              <button
                type="submit"
                disabled={loading}
                style={{
                  padding: "0.6rem 1.1rem",
                  borderRadius: "0.5rem",
                  border: "none",
                  cursor: loading ? "default" : "pointer",
                  background: loading ? "#6b7280" : "#22c55e",
                  color: "#020617",
                  fontWeight: 700,
                  fontSize: "0.9rem",
                  whiteSpace: "nowrap",
                }}
              >
                {loading ? "Scraping..." : "Scrape"}
              </button>
            </div>

            <div
              style={{
                display: "flex",
                gap: "0.75rem",
                flexWrap: "wrap",
                alignItems: "center",
                fontSize: "0.8rem",
              }}
            >
              <div style={{ display: "flex", gap: "0.25rem", alignItems: "center" }}>
                <span style={{ color: "#cbd5f5" }}>Mode:</span>
                <select
                  value={mode}
                  onChange={(e) => setMode(e.target.value)}
                  style={{
                    padding: "0.25rem 0.4rem",
                    borderRadius: "0.4rem",
                    border: "1px solid #1f2937",
                    background: "#020617",
                    color: "#e5e7eb",
                  }}
                >
                  <option value="auto">auto (static → js)</option>
                  <option value="static">static only</option>
                  <option value="js">js only (with static fallback)</option>
                </select>
              </div>

              <label
                style={{
                  display: "flex",
                  gap: "0.35rem",
                  alignItems: "center",
                  cursor: "pointer",
                }}
              >
                <input
                  type="checkbox"
                  checked={deep}
                  onChange={(e) => setDeep(e.target.checked)}
                />
                <span>Deep crawl (more scroll & pages)</span>
              </label>

              <button
                type="button"
                onClick={() => setShowRawJson((s) => !s)}
                style={{
                  marginLeft: "auto",
                  borderRadius: "999px",
                  padding: "0.3rem 0.7rem",
                  border: "1px solid #1f2937",
                  background: "#020617",
                  color: "#e5e7eb",
                  cursor: "pointer",
                }}
              >
                {showRawJson ? "Hide Raw JSON" : "Show Raw JSON"}
              </button>
            </div>
          </form>
        </section>

        {error && (
          <div
            style={{
              marginBottom: "1rem",
              padding: "0.75rem 1rem",
              borderRadius: "0.75rem",
              background: "#7f1d1d",
              color: "#fee2e2",
              fontSize: "0.85rem",
              border: "1px solid #b91c1c",
            }}
          >
            {error}
          </div>
        )}

        {result && (
          <>
            <section
              style={{
                marginBottom: "1rem",
                padding: "0.9rem 1rem",
                borderRadius: "0.75rem",
                background: "#020617",
                border: "1px solid #1f2937",
              }}
            >
              <div
                style={{
                  display: "flex",
                  flexWrap: "wrap",
                  gap: "0.75rem",
                  justifyContent: "space-between",
                  alignItems: "center",
                }}
              >
                <div style={{ fontSize: "0.8rem", color: "#9ca3af" }}>
                  <div style={{ marginBottom: "0.15rem" }}>
                    <strong>URL: </strong>
                    <span style={{ color: "#e5e7eb" }}>{result.url}</span>
                  </div>
                  <div style={{ marginBottom: "0.15rem" }}>
                    <strong>Scraped at: </strong>
                    <span style={{ color: "#e5e7eb" }}>
                      {result.scrapedAt}
                    </span>
                  </div>
                  <div>
                    <strong>Strategy: </strong>
                    <span style={{ color: "#e5e7eb" }}>
                      {result.meta?.strategy || "unknown"}
                    </span>
                  </div>
                </div>
                <div
                  style={{
                    display: "flex",
                    gap: "0.5rem",
                    alignItems: "center",
                  }}
                >
                  <div
                    style={{
                      fontSize: "0.75rem",
                      color: "#9ca3af",
                      textAlign: "right",
                    }}
                  >
                    <div>
                      <strong>Sections:</strong>{" "}
                      {result.sections ? result.sections.length : 0}
                    </div>
                    <div>
                      <strong>Scrolls:</strong>{" "}
                      {result.interactions?.scrolls ?? 0}
                    </div>
                    <div>
                      <strong>Clicks:</strong>{" "}
                      {(result.interactions?.clicks || []).length}
                    </div>
                  </div>
                  <button
                    type="button"
                    onClick={handleDownload}
                    style={{
                      padding: "0.5rem 0.8rem",
                      borderRadius: "0.5rem",
                      border: "1px solid #60a5fa",
                      background: "#0b1120",
                      color: "#bfdbfe",
                      cursor: "pointer",
                      fontSize: "0.8rem",
                      whiteSpace: "nowrap",
                    }}
                  >
                    Download JSON
                  </button>
                </div>
              </div>
            </section>

            <SectionList sections={result.sections || []} />

            {showRawJson && (
              <>
                <h2
                  style={{
                    marginTop: "1.5rem",
                    marginBottom: "0.5rem",
                    fontSize: "1.1rem",
                  }}
                >
                  Raw Result JSON
                </h2>
                <JsonViewer data={result} />
              </>
            )}

            {result.interactions && result.interactions.timeline && (
              <>
                <h2
                  style={{
                    marginTop: "1.5rem",
                    marginBottom: "0.5rem",
                    fontSize: "1.05rem",
                  }}
                >
                  Interaction Timeline
                </h2>
                <div
                  style={{
                    borderRadius: "0.75rem",
                    border: "1px solid #1f2937",
                    padding: "0.75rem",
                    fontSize: "0.78rem",
                    background: "#020617",
                  }}
                >
                  {result.interactions.timeline.length === 0 && (
                    <div style={{ color: "#6b7280" }}>No events recorded.</div>
                  )}
                  {result.interactions.timeline.map((ev, idx) => (
                    <div
                      key={idx}
                      style={{
                        display: "flex",
                        flexWrap: "wrap",
                        gap: "0.4rem",
                        marginBottom: "0.35rem",
                      }}
                    >
                      <span style={{ color: "#9ca3af" }}>{ev.time}</span>
                      <span
                        style={{
                          padding: "0.1rem 0.4rem",
                          borderRadius: "999px",
                          border: "1px solid #1f2937",
                          textTransform: "uppercase",
                          fontSize: "0.7rem",
                        }}
                      >
                        {ev.event}
                      </span>
                      <span>{ev.description}</span>
                      {ev.url && (
                        <span style={{ color: "#60a5fa" }}>
                          ({ev.url})
                        </span>
                      )}
                    </div>
                  ))}
                </div>
              </>
            )}

            {result.errors && result.errors.length > 0 && (
              <>
                <h2
                  style={{
                    marginTop: "1.5rem",
                    marginBottom: "0.5rem",
                    fontSize: "1.05rem",
                  }}
                >
                  Errors
                </h2>
                <div
                  style={{
                    borderRadius: "0.75rem",
                    border: "1px solid #7f1d1d",
                    padding: "0.75rem",
                    background: "#450a0a",
                    fontSize: "0.78rem",
                  }}
                >
                  {result.errors.map((err, idx) => (
                    <div key={idx} style={{ marginBottom: "0.35rem" }}>
                      <strong>[{err.phase}]</strong>{" "}
                      {err.kind && <span>({err.kind}) </span>}
                      {err.message}
                    </div>
                  ))}
                </div>
              </>
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default App;