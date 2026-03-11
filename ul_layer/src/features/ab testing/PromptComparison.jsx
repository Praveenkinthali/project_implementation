export default function PromptComparison({ originalPrompt, optimizedPrompt }) {

  return (

    <div style={styles.container}>

      <h3 style={styles.title}>Prompts</h3>

      <div style={styles.grid}>

        <div style={styles.card}>

          <div style={styles.cardTitle}>Original Prompt</div>

          <div style={styles.promptBox}>
            {originalPrompt || "No prompt"}
          </div>

        </div>

        <div style={styles.card}>

          <div style={styles.cardTitle}>Optimized Prompt</div>

          <div style={styles.promptBox}>
            {optimizedPrompt || "No prompt"}
          </div>

        </div>

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
    fontSize:"13px",
    fontWeight:"600",
    marginBottom:"4px"
  },

  promptBox:{
  flex:1,
  background:"#f3f4f6",
  padding:"12px",
  borderRadius:"6px",
  overflowY:"auto",
  whiteSpace:"pre-wrap",
  fontSize:"13px"
}

};