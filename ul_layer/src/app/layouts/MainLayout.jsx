import { Outlet } from "react-router-dom";

export default function MainLayout() {
  return (
    <div style={styles.container}>
      <Outlet />
    </div>
  );
}

const styles = {
  container: {
    display: "flex",
    height: "100vh",
    backgroundColor: "#f7f7f8",
  },
};