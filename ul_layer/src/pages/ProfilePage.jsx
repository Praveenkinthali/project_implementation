import { useEffect, useState } from "react";

export default function ProfilePage() {

  const [user, setUser] = useState({
    name: "",
    email: ""
  });

  useEffect(() => {

    const email = localStorage.getItem("user_email");

    if (email) {
      setUser({
        name: email.split("@")[0],
        email: email
      });
    }

  }, []);

  return (

    <div style={styles.wrapper}>

      <div style={styles.container}>

        <h1 style={styles.title}>Profile</h1>

        <div style={styles.card}>

          <div style={styles.avatar}>
            {user.name.charAt(0).toUpperCase()}
          </div>

          <div style={styles.userInfo}>

            <div style={styles.row}>
              <span style={styles.label}>Full Name</span>
              <span style={styles.value}>{user.name}</span>
            </div>

            <div style={styles.row}>
              <span style={styles.label}>Email Address</span>
              <span style={styles.value}>{user.email}</span>
            </div>

            <div style={styles.row}>
              <span style={styles.label}>Account Type</span>
              <span style={styles.value}>Standard User</span>
            </div>

            <div style={styles.row}>
              <span style={styles.label}>Member Since</span>
              <span style={styles.value}>2025</span>
            </div>

          </div>

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
    gap: "25px",
    alignItems: "center"
  },

  avatar: {
    width: "80px",
    height: "80px",
    borderRadius: "50%",
    background: "#2563eb",
    color: "white",
    fontSize: "32px",
    fontWeight: "600",
    display: "flex",
    alignItems: "center",
    justifyContent: "center"
  },

  userInfo: {
    flex: 1
  },

  row: {
    display: "flex",
    justifyContent: "space-between",
    padding: "8px 0",
    borderBottom: "1px solid #eee"
  },

  label: {
    color: "#666",
    fontWeight: "500"
  },

  value: {
    fontWeight: "500"
  }

};