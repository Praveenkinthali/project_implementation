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

  const promptMetrics = evaluation?.metrics?.prompt_metrics || {};
  const primitiveMetrics = evaluation?.metrics?.primitive_metrics || {};

  const instruction = promptMetrics?.instruction_metrics || {};
  const constraint = promptMetrics?.constraint_metrics || {};
  const format = promptMetrics?.format_metrics || {};
  const structure = promptMetrics?.structural_metrics || {};

  const primitives =
    primitiveMetrics?.usage_metrics?.total_primitives_used
      ? primitiveMetrics?.usage_metrics
      : null;

  const primitivesList =
    evaluation?.metadata?.primitives || [];

  const improvements = [
    instruction.instruction_density_delta || 0,
    constraint.constraint_delta || 0,
    (format.optimized_format_markers || 0) -
      (format.original_format_markers || 0),
    structure.structural_change_score || 0
  ];

  const improvedCount =
    improvements.filter(v => v > 0).length;

  return (
    <div style={styles.panel}>

      <h3>Prompt Evaluation</h3>

      {/* FINAL SCORE */}

      <div style={styles.scoreSection}>
        <div style={styles.scoreHeader}>
          <span>Final Score</span>
          <span>{scorePercent}%</span>
        </div>

        <div style={styles.progressBar}>
          <div
            style={{
              ...styles.progressFill,
              width: `${scorePercent}%`
            }}
          />
        </div>
      </div>

      {/* OPTIMIZATION SUMMARY */}

      <div style={styles.summaryBox}>
        Improved Metrics: {improvedCount} / 4
      </div>

      {/* PROMPT METRIC COMPARISON */}

      <h4 style={styles.sectionTitle}>
        Prompt Metrics Comparison
      </h4>

      <BarComparison
        label="Instruction Count"
        original={instruction.original_instruction_count}
        optimized={instruction.optimized_instruction_count}
      />

      <BarComparison
        label="Constraint Count"
        original={constraint.original_constraint_count}
        optimized={constraint.optimized_constraint_count}
      />

      <BarComparison
        label="Formatting Markers"
        original={format.original_format_markers}
        optimized={format.optimized_format_markers}
      />

      {/* STRUCTURAL CHANGE */}

      <ImprovementBar
        label="Structural Change"
        value={structure.structural_change_score}
        max={1}
      />

      {/* PRIMITIVE USAGE */}

      {primitivesList.length > 0 && (
        <>
          <h4 style={styles.sectionTitle}>
            Primitives Applied
          </h4>

          <div style={styles.primitiveList}>
            {primitivesList.map((p, i) => (
              <span key={i} style={styles.primitiveBadge}>
                {p}
              </span>
            ))}
          </div>
        </>
      )}

    </div>
  );
}


/* ORIGINAL vs OPTIMIZED BAR */

function BarComparison({ label, original = 0, optimized = 0 }) {

  const max = Math.max(original, optimized, 1);

  const origWidth = (original / max) * 100;
  const optWidth = (optimized / max) * 100;

  const improved = optimized > original;

  return (
    <div style={styles.metricBlock}>

      <div style={styles.metricLabel}>
        {label}
      </div>

      <div style={styles.barRow}>
        <span style={styles.barTitle}>O</span>

        <div style={styles.barContainer}>
          <div
            style={{
              ...styles.barOriginal,
              width: `${origWidth}%`
            }}
          />
        </div>

        <span>{original}</span>
      </div>

      <div style={styles.barRow}>
        <span style={styles.barTitle}>Opt</span>

        <div style={styles.barContainer}>
          <div
            style={{
              ...styles.barOptimized,
              width: `${optWidth}%`
            }}
          />
        </div>

        <span>
          {optimized}
          {improved && (
            <span style={styles.upArrow}> ↑</span>
          )}
        </span>
      </div>

    </div>
  );
}


/* IMPROVEMENT BAR */

function ImprovementBar({ label, value = 0, max = 1 }) {

  const width = (value / max) * 100;

  return (
    <div style={styles.metricBlock}>

      <div style={styles.metricLabel}>
        {label}
      </div>

      <div style={styles.barRow}>
        <div style={styles.barContainer}>
          <div
            style={{
              ...styles.barImprovement,
              width: `${width}%`
            }}
          />
        </div>

        <span>{value.toFixed(2)}</span>
      </div>

    </div>
  );
}


const styles = {

  panel: {
    width: "380px",
    padding: "24px",
    borderLeft: "1px solid #ddd",
    backgroundColor: "white"
  },

  scoreSection: {
    marginBottom: "16px"
  },

  scoreHeader: {
    display: "flex",
    justifyContent: "space-between",
    marginBottom: "6px",
    fontWeight: "600"
  },

  progressBar: {
    height: "10px",
    background: "#eee",
    borderRadius: "6px",
    overflow: "hidden"
  },

  progressFill: {
    height: "100%",
    background: "#2563eb"
  },

  summaryBox:{
    background:"#f1f5f9",
    padding:"8px",
    borderRadius:"6px",
    fontSize:"13px",
    marginBottom:"12px"
  },

  sectionTitle:{
    marginTop:"18px",
    marginBottom:"10px",
    fontSize:"14px"
  },

  metricBlock:{
    marginBottom:"10px"
  },

  metricLabel:{
    fontSize:"13px",
    marginBottom:"4px"
  },

  barRow:{
    display:"flex",
    alignItems:"center",
    gap:"6px",
    marginBottom:"4px"
  },

  barTitle:{
    width:"26px",
    fontSize:"12px"
  },

  barContainer:{
    flex:1,
    height:"8px",
    background:"#eee",
    borderRadius:"5px",
    overflow:"hidden"
  },

  barOriginal:{
    height:"100%",
    background:"#9ca3af"
  },

  barOptimized:{
    height:"100%",
    background:"#2563eb"
  },

  barImprovement:{
    height:"100%",
    background:"#16a34a"
  },

  upArrow:{
    color:"#16a34a",
    marginLeft:"4px"
  },

  primitiveList:{
    display:"flex",
    flexWrap:"wrap",
    gap:"6px"
  },

  primitiveBadge:{
    background:"#e2e8f0",
    padding:"4px 8px",
    borderRadius:"4px",
    fontSize:"12px"
  }

};