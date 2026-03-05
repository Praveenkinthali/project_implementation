export default function Navbar() {
  return (
    <div style={styles.navbar}>
      <h2>Workspace</h2>
    </div>
  );
}

const styles = {
  navbar: {
    height: "60px",
    borderBottom: "1px solid #ddd",
    display: "flex",
    alignItems: "center",
    paddingLeft: "20px",
    backgroundColor: "white",
  },
};