import { useNavigate } from "react-router-dom";

export default function SettingsPage() {

  const navigate = useNavigate();
  const email = localStorage.getItem("user_email");

  const handleLogout = () => {

    localStorage.removeItem("token");
    localStorage.removeItem("user_email");

    navigate("/login");

  };

  return (

    <div style={styles.wrapper}>

      <div style={styles.container}>

        <h1 style={styles.title}>Settings</h1>

        <div style={styles.card}>

          <h3 style={styles.sectionTitle}>Account</h3>

          <div style={styles.row}>
            <span>Email</span>
            <span>{email}</span>
          </div>

          <div style={styles.row}>
            <span>Password</span>
            <span>••••••••</span>
          </div>

          <h3 style={styles.sectionTitle}>Preferences</h3>

          <div style={styles.row}>
            <span>Theme</span>
            <span>Light</span>
          </div>

          <div style={styles.row}>
            <span>Notifications</span>
            <span>Enabled</span>
          </div>

          <button
            onClick={handleLogout}
            style={styles.logoutButton}
          >
            Logout
          </button>

        </div>

      </div>

    </div>

  );
}

const styles = {

  wrapper: {
    flex: 1,
    display: "flex",
    justifyContent: "center",
    alignItems: "flex-start",
    paddingTop: "60px",
    background: "#f5f7fb"
  },

  container: {
    width: "600px"
  },

  title: {
    fontSize: "30px",
    fontWeight: "600",
    marginBottom: "25px"
  },

  card: {
    background: "white",
    padding: "35px",
    borderRadius: "12px",
    boxShadow: "0 8px 25px rgba(0,0,0,0.08)",
    display: "flex",
    flexDirection: "column",
    gap: "15px"
  },

  sectionTitle: {
    marginTop: "10px",
    marginBottom: "5px",
    fontSize: "18px",
    fontWeight: "600"
  },

  row: {
    display: "flex",
    justifyContent: "space-between",
    padding: "8px 0",
    borderBottom: "1px solid #eee"
  },

  logoutButton: {
    marginTop: "20px",
    padding: "12px",
    borderRadius: "8px",
    border: "none",
    background: "#ef4444",
    color: "white",
    fontWeight: "500",
    cursor: "pointer"
  }

};