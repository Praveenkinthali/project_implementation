export default function MetricsComparison({ resultA, resultB }) {

  const respA =
    resultA?.evaluation?.response_analysis?.response_metrics || {};

  const respB =
    resultB?.evaluation?.response_analysis?.response_metrics || {};

  const semA =
    resultA?.evaluation?.response_analysis?.semantic_metrics || {};

  const semB =
    resultB?.evaluation?.response_analysis?.semantic_metrics || {};

  const judgeA =
    resultA?.evaluation?.response_analysis?.judge_metrics || {};

  const judgeB =
    resultB?.evaluation?.response_analysis?.judge_metrics || {};

  /* EXISTING METRICS */

  const relevanceA =
    respA?.relevance_metrics?.keyword_overlap_score || 0;

  const relevanceB =
    respB?.relevance_metrics?.keyword_overlap_score || 0;

  const adherenceA =
    respA?.instruction_adherence?.instruction_adherence_score || 0;

  const adherenceB =
    respB?.instruction_adherence?.instruction_adherence_score || 0;

  const structureA =
    respA?.structure_metrics?.list_structure_delta || 0;

  const structureB =
    respB?.structure_metrics?.list_structure_delta || 0;

  const alignmentA =
    semA?.prompt_response_alignment || 0;

  const alignmentB =
    semB?.prompt_response_alignment || 0;

  const semanticA =
    semA?.prompt_semantic_similarity || 0;

  const semanticB =
    semB?.prompt_semantic_similarity || 0;

  const judgeScoreA =
    ((judgeA?.clarity || 0) +
     (judgeA?.relevance || 0) +
     (judgeA?.completeness || 0) +
     (judgeA?.factual_reliability || 0)) / 40;

  const judgeScoreB =
    ((judgeB?.clarity || 0) +
     (judgeB?.relevance || 0) +
     (judgeB?.completeness || 0) +
     (judgeB?.factual_reliability || 0)) / 40;

  return (

    <div style={styles.container}>

      <h3 style={styles.title}>Response Comparison</h3>

      <table style={styles.table}>

        <thead>
          <tr>
            <th>Metric</th>
            <th style={styles.center}>Original</th>
            <th style={styles.center}>Optimized</th>
          </tr>
        </thead>

        <tbody>

          <Row
            name="Keyword Relevance"
            a={`${Math.round(relevanceA*100)}%`}
            b={`${Math.round(relevanceB*100)}%`}
          />

          <Row
            name="Instruction Adherence"
            a={`${Math.round(adherenceA*100)}%`}
            b={`${Math.round(adherenceB*100)}%`}
          />

          <Row
            name="Structure Score"
            a={`${Math.round(structureA*100)}%`}
            b={`${Math.round(structureB*100)}%`}
          />

          <Row
            name="Prompt-Response Alignment"
            a={`${Math.round(alignmentA*100)}%`}
            b={`${Math.round(alignmentB*100)}%`}
          />

          <Row
            name="Semantic Similarity"
            a={`${Math.round(semanticA*100)}%`}
            b={`${Math.round(semanticB*100)}%`}
          />

          <Row
            name="LLM Judge Score"
            a={`${Math.round(judgeScoreA*100)}%`}
            b={`${Math.round(judgeScoreB*100)}%`}
          />

        </tbody>

      </table>

    </div>

  );
}

function Row({ name, a, b }) {

  return (
    <tr>
      <td>{name}</td>
      <td style={{textAlign:"center"}}>{a}</td>
      <td style={{textAlign:"center"}}>{b}</td>
    </tr>
  );

}

const styles = {

  container:{
    height:"100%",
    overflowY:"auto"
  },

  title:{
    marginBottom:"12px",
    fontWeight:"600"
  },

  table:{
    width:"100%",
    borderCollapse:"collapse",
    fontSize:"14px"
  },

  center:{
    textAlign:"center"
  }

};