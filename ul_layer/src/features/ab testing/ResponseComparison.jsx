import ReactMarkdown from "react-markdown";

export default function ResponseComparison({ resultA, resultB, loading }) {

  return (

    <div style={styles.container}>

      <h3 style={styles.title}>Responses</h3>

      <div style={styles.grid}>

        <ResponseCard
          title="Response A"
          result={resultA}
          loading={loading}
        />

        <ResponseCard
          title="Response B"
          result={resultB}
          loading={loading}
        />

      </div>

    </div>

  );
}

function ResponseCard({ title, result, loading }) {

  return (

    <div style={styles.card}>

      <div style={styles.cardTitle}>{title}</div>

      <div style={styles.responseBox}>

        {loading && (
          <div style={styles.loading}>Generating...</div>
        )}

        {!loading && result && (
          <ReactMarkdown>
            {result.optimized_response || result.response}
          </ReactMarkdown>
        )}

        {!loading && !result && (
          <div style={styles.empty}>
            Click Run A/B Comparison
          </div>
        )}

      </div>

    </div>

  );

}

const styles = {

  container:{
    display:"flex",
    flexDirection:"column",
    height:"100%"
  },

  title:{
    marginBottom:"6px",
    fontWeight:"600"
  },

  grid:{
    display:"grid",
    gridTemplateColumns:"1fr 1fr",
    gap:"12px",
    flex:1,
    minHeight:0
  },

  card:{
    display:"flex",
    flexDirection:"column",
    minHeight:0
  },

  cardTitle:{
    fontWeight:"600",
    marginBottom:"4px"
  },

  responseBox:{
  flex:1,
  background:"#fafafa",
  padding:"14px",
  borderRadius:"6px",
  overflowY:"auto",
  fontSize:"13px",
  lineHeight:"1.6"
},

  loading:{
    textAlign:"center",
    padding:"20px"
  },

  empty:{
    textAlign:"center",
    color:"#999"
  }

};