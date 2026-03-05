import { useLocation, useNavigate } from "react-router-dom";
import { useState } from "react";
import ReactMarkdown from "react-markdown";
import api from "../api/axiosConfig";

export default function ABTestingPage() {

  const location = useLocation();
  const navigate = useNavigate();

  const { originalPrompt, optimizedPrompt } =
    location.state || {};

  const [resultA, setResultA] = useState(null);
  const [resultB, setResultB] = useState(null);
  const [loading, setLoading] = useState(false);

  const runComparison = async () => {

    if (!originalPrompt || !optimizedPrompt) return;

    setLoading(true);

    try {

      const resA = await api.post("/generate", {
        prompt: originalPrompt,
      });

      const resB = await api.post("/generate", {
        prompt: optimizedPrompt,
      });

      setResultA(resA.data);
      setResultB(resB.data);

    } catch (err) {
      console.error("A/B error:", err);
    }

    setLoading(false);
  };

  const winner =
    resultA && resultB
      ? resultA.tokens < resultB.tokens
        ? "A"
        : "B"
      : null;

  return (

    <div style={styles.page}>

      {/* HEADER */}

      <div style={styles.header}>

        <h2 style={styles.title}>A/B Prompt Comparison</h2>

        <button
          style={styles.backBtn}
          onClick={() => navigate("/chat")}
        >
          Back to Chat
        </button>

      </div>

      {/* RUN BUTTON */}

      <button
        style={styles.runBtn}
        onClick={runComparison}
      >
        Run Comparison
      </button>

      {loading && (
        <p style={styles.loading}>
          Running comparison...
        </p>
      )}

      {/* GRID */}

      <div style={styles.grid}>

        {/* PROMPT A */}

        <div
          style={{
            ...styles.card,
            border:
              winner === "A"
                ? "2px solid #22c55e"
                : "1px solid #ddd",
          }}
        >

          <h3 style={styles.cardTitle}>
            Prompt A {winner === "A" && "🏆"}
          </h3>

          <div style={styles.promptBox}>
            {originalPrompt}
          </div>

          {resultA && (
            <>
              <h4 style={styles.sectionTitle}>
                Response
              </h4>

              <div style={styles.responseBox}>
                <ReactMarkdown>
                  {resultA.response}
                </ReactMarkdown>
              </div>

              <div style={styles.metrics}>
                <span>
                  Tokens: {resultA.tokens}
                </span>

                <span>
                  Latency: {resultA.latency}s
                </span>
              </div>
            </>
          )}

        </div>

        {/* PROMPT B */}

        <div
          style={{
            ...styles.card,
            border:
              winner === "B"
                ? "2px solid #22c55e"
                : "1px solid #ddd",
          }}
        >

          <h3 style={styles.cardTitle}>
            Prompt B {winner === "B" && "🏆"}
          </h3>

          <div style={styles.promptBox}>
            {optimizedPrompt}
          </div>

          {resultB && (
            <>
              <h4 style={styles.sectionTitle}>
                Response
              </h4>

              <div style={styles.responseBox}>
                <ReactMarkdown>
                  {resultB.response}
                </ReactMarkdown>
              </div>

              <div style={styles.metrics}>
                <span>
                  Tokens: {resultB.tokens}
                </span>

                <span>
                  Latency: {resultB.latency}s
                </span>
              </div>
            </>
          )}

        </div>

      </div>

    </div>

  );
}

const styles = {

  page: {
    flex: 1,
    padding: "40px",
    background: "#f5f7fb",
  },

  header: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: "25px",
  },

  title: {
    fontSize: "26px",
    fontWeight: "600",
  },

  backBtn: {
    padding: "8px 14px",
    borderRadius: "6px",
    border: "1px solid #ccc",
    cursor: "pointer",
    background: "white",
  },

  runBtn: {
    padding: "10px 20px",
    marginBottom: "30px",
    borderRadius: "8px",
    border: "none",
    background: "#2563eb",
    color: "white",
    cursor: "pointer",
    fontWeight: "500",
  },

  loading: {
    marginBottom: "20px",
    color: "#555",
  },

  grid: {
    display: "grid",
    gridTemplateColumns: "1fr 1fr",
    gap: "25px",
  },

  card: {
    background: "white",
    padding: "22px",
    borderRadius: "12px",
    boxShadow: "0 4px 18px rgba(0,0,0,0.08)",
  },

  cardTitle: {
    marginBottom: "12px",
  },

  sectionTitle: {
    marginBottom: "10px",
  },

  promptBox: {
    background: "#f3f4f6",
    padding: "12px",
    borderRadius: "6px",
    marginBottom: "15px",
    whiteSpace: "pre-wrap",
  },

  responseBox: {
    background: "#fafafa",
    padding: "15px",
    borderRadius: "8px",
    marginBottom: "12px",
    minHeight: "120px",
    lineHeight: "1.6",
    fontSize: "14px",
  },

  metrics: {
    display: "flex",
    justifyContent: "space-between",
    fontSize: "14px",
    color: "#444",
  },

};