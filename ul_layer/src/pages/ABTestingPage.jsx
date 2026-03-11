import { useLocation, useNavigate } from "react-router-dom";
import { useState } from "react";
import api from "../api/axiosConfig";

import PromptComparison from "../features/ab testing/PromptComparison";
import ResponseComparison from "../features/ab testing/ResponseComparison";
import MetricsComparison from "../features/ab testing/MetricsComparison";

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

      const resA = await api.post("/optimize", {
        prompt: originalPrompt
      });

      const resB = await api.post("/optimize", {
        prompt: optimizedPrompt
      });

      setResultA(resA.data);
      setResultB(resB.data);

    } catch (err) {
      console.error("AB error:", err);
    }

    setLoading(false);
  };

  return (

    <div style={styles.page}>

      {/* NAVBAR */}

      <div style={styles.header}>

        <div style={styles.left}>
          <h1 style={styles.logo}>SRPP STUDIO</h1>
        </div>

        <div style={styles.center}>
          <button
            style={styles.runBtn}
            onClick={runComparison}
            disabled={loading}
          >
            {loading ? "Running..." : "Run A/B Test"}
          </button>
        </div>

        <div style={styles.right}>
          <button
            style={styles.backBtn}
            onClick={() => navigate("/chat")}
          >
            Back
          </button>
        </div>

      </div>

      {/* DASHBOARD */}

      <div style={styles.dashboard}>

        <div style={styles.block}>
          <PromptComparison
            originalPrompt={originalPrompt}
            optimizedPrompt={optimizedPrompt}
          />
        </div>

        <div style={styles.block}>
          <ResponseComparison
            resultA={resultA}
            resultB={resultB}
            loading={loading}
          />
        </div>

        <div style={styles.block}>
          <MetricsComparison
            resultA={resultA}
            resultB={resultB}
          />
        </div>

      </div>

    </div>

  );
}

const styles = {

  page:{
    height:"100vh",
    width:"100vw",
    display:"flex",
    flexDirection:"column",
    background:"#f5f7fb",
    overflow:"hidden"
  },

  header:{
    display:"grid",
    gridTemplateColumns:"1fr 1fr 1fr",
    alignItems:"center",
    padding:"14px 30px",
    borderBottom:"1px solid #ddd",
    background:"white"
  },

  left:{ textAlign:"left" },
  center:{ textAlign:"center" },
  right:{ textAlign:"right" },

  logo:{
    fontSize:"22px",
    fontWeight:"700"
  },

  runBtn:{
    padding:"8px 20px",
    background:"#2563eb",
    color:"white",
    border:"none",
    borderRadius:"6px",
    cursor:"pointer"
  },

  backBtn:{
    padding:"8px 14px",
    border:"1px solid #ccc",
    background:"white",
    borderRadius:"6px",
    cursor:"pointer"
  },

  dashboard:{
    flex:1,
    display:"grid",
    gridTemplateRows:"0.8fr 2.3fr 1fr",
    gap:"10px",
    padding:"12px",
    overflow:"hidden"
  },

  block:{
    background:"white",
    borderRadius:"8px",
    padding:"14px",
    display:"flex",
    flexDirection:"column",
    minHeight:0,
    overflow:"hidden",
    border:"1px solid #e5e7eb"
  }

};