export default function EvaluationPanel({ evaluation }) {
  if (!evaluation) {
    return (
      <div style={styles.panel}>
        <h3>Evaluation</h3>
        <p>No evaluation yet.</p>
      </div>
    );
  }

  const scorePercent = Math.round(evaluation.final_score * 100);

  return (
    <div style={styles.panel}>
      <h3>Evaluation</h3>

      <div style={styles.scoreSection}>
        <div style={styles.scoreHeader}>
          <span>Final Score</span>
          <span>{scorePercent}%</span>
        </div>

        <div style={styles.progressBar}>
          <div
            style={{
              ...styles.progressFill,
              width: `${scorePercent}%`,
              backgroundColor:
                scorePercent > 80
                  ? "#16a34a"
                  : scorePercent > 50
                  ? "#eab308"
                  : "#dc2626",
            }}
          />
        </div>
      </div>

      <div style={styles.metricRow}>
        <strong>Should Iterate</strong>
        <span
          style={{
            color: evaluation.should_iterate ? "#dc2626" : "#16a34a",
            fontWeight: "bold",
          }}
        >
          {evaluation.should_iterate ? "Yes" : "No"}
        </span>
      </div>
    </div>
  );
}

const styles = {
  panel: {
    width: "320px",
    padding: "24px",
    borderLeft: "1px solid #ddd",
    backgroundColor: "white",
  },

  scoreSection: {
    marginBottom: "20px",
  },

  scoreHeader: {
    display: "flex",
    justifyContent: "space-between",
    marginBottom: "8px",
    fontWeight: "500",
  },

  progressBar: {
    height: "10px",
    backgroundColor: "#eee",
    borderRadius: "8px",
    overflow: "hidden",
  },

  progressFill: {
    height: "100%",
    borderRadius: "8px",
  },

  metricRow: {
    display: "flex",
    justifyContent: "space-between",
    marginTop: "10px",
  },
};