import React from "react";

const JsonViewer = ({ data }) => {
  return (
    <pre
      style={{
        background: "#0b1120",
        color: "#e5e7eb",
        padding: "0.75rem",
        borderRadius: "0.75rem",
        fontSize: "0.78rem",
        overflowX: "auto",
        border: "1px solid #111827",
      }}
    >
      {JSON.stringify(data, null, 2)}
    </pre>
  );
};

export default JsonViewer;