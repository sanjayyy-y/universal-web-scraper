import React, { useState } from "react";
import JsonViewer from "./JsonViewer";

const SectionList = ({ sections }) => {
  const [openId, setOpenId] = useState(null);

  if (!sections.length) {
    return (
      <p style={{ color: "#9ca3af", fontSize: "0.85rem", marginTop: "1rem" }}>
        No sections extracted.
      </p>
    );
  }

  return (
    <section style={{ marginTop: "1rem" }}>
      <h2 style={{ marginBottom: "0.5rem", fontSize: "1.05rem" }}>Sections</h2>
      <div style={{ display: "flex", flexDirection: "column", gap: "0.6rem" }}>
        {sections.map((section) => {
          const isOpen = openId === section.id;
          return (
            <div
              key={section.id}
              style={{
                borderRadius: "0.75rem",
                border: "1px solid #1f2937",
                overflow: "hidden",
                background: "#020617",
              }}
            >
              <button
                type="button"
                onClick={() => setOpenId(isOpen ? null : section.id)}
                style={{
                  width: "100%",
                  padding: "0.6rem 0.9rem",
                  border: "none",
                  background: isOpen ? "#0b1120" : "#020617",
                  color: "#e5e7eb",
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                  cursor: "pointer",
                  fontSize: "0.9rem",
                }}
              >
                <div style={{ display: "flex", flexDirection: "column" }}>
                  <span style={{ fontWeight: 600 }}>
                    {section.label || section.id}
                  </span>
                  <span style={{ fontSize: "0.75rem", color: "#9ca3af" }}>
                    {section.sourceUrl}
                  </span>
                </div>
                <div style={{ textAlign: "right", fontSize: "0.75rem" }}>
                  <span
                    style={{
                      textTransform: "uppercase",
                      borderRadius: "999px",
                      border: "1px solid #1f2937",
                      padding: "0.1rem 0.45rem",
                      marginRight: "0.4rem",
                    }}
                  >
                    {section.type}
                  </span>
                  <span style={{ color: "#9ca3af" }}>
                    {section.truncated ? "HTML truncated" : "Full HTML"}
                  </span>
                </div>
              </button>
              {isOpen && (
                <div
                  style={{
                    padding: "0.7rem 0.9rem",
                    background: "#020617",
                  }}
                >
                  <JsonViewer data={section} />
                </div>
              )}
            </div>
          );
        })}
      </div>
    </section>
  );
};

export default SectionList;