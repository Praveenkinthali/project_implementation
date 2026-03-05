import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/axiosConfig";

export default function LoginPage() {

  const navigate = useNavigate();

  const [isLogin, setIsLogin] = useState(true);
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);

  const toggleMode = () => {
    setIsLogin(!isLogin);
    setName("");
    setEmail("");
    setPassword("");
    setShowPassword(false);
  };

  const handleSubmit = async () => {

    if (!email || !password || (!isLogin && !name)) {
      alert("Please fill all required fields");
      return;
    }

    try {

      let res;

      if (isLogin) {

        res = await api.post("/auth/login", {
          email,
          password,
        });

      } else {

        await api.post("/auth/register", {
          name,
          email,
          password,
        });

        res = await api.post("/auth/login", {
          email,
          password,
        });

      }

      const token = res.data.access_token;

      localStorage.setItem("token", token);
      localStorage.setItem("user_email", email);

      navigate("/chat");

    } catch (err) {

      console.error(err);

      alert(err.response?.data?.detail || "Authentication failed");

    }
  };

  const handleGoogleLogin = () => {
    alert("Google login coming next step 🚀");
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>

        <h2>{isLogin ? "Login to SRPP Studio" : "Create Account"}</h2>

        {!isLogin && (
          <input
            type="text"
            placeholder="Enter name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            style={styles.input}
          />
        )}

        <input
          type="email"
          placeholder="Enter email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          style={styles.input}
        />

        <div style={{ position: "relative" }}>
          <input
            type={showPassword ? "text" : "password"}
            placeholder="Enter password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            style={styles.input}
          />

          <button
            type="button"
            onClick={() => setShowPassword(!showPassword)}
            style={styles.eyeButton}
          >
            👁
          </button>
        </div>

        <button onClick={handleSubmit} style={styles.primaryButton}>
          {isLogin ? "Login" : "Sign Up"}
        </button>

        <div style={styles.divider}>OR</div>

        <button onClick={handleGoogleLogin} style={styles.googleButton}>
          Continue with Google
        </button>

        <p style={styles.toggleText}>
          {isLogin ? "Don't have an account?" : "Already have an account?"}

          <span style={styles.link} onClick={toggleMode}>
            {isLogin ? " Sign Up" : " Login"}
          </span>
        </p>

      </div>
    </div>
  );
}

const styles = {

  container: {
    height: "100vh",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#f4f6f8",
  },

  card: {
    width: "350px",
    padding: "30px",
    borderRadius: "12px",
    backgroundColor: "white",
    boxShadow: "0 8px 20px rgba(0,0,0,0.08)",
    display: "flex",
    flexDirection: "column",
    gap: "15px",
  },

  input: {
    padding: "12px",
    borderRadius: "8px",
    border: "1px solid #ddd",
    width: "100%",
  },

  primaryButton: {
    padding: "12px",
    borderRadius: "8px",
    border: "none",
    backgroundColor: "#2563eb",
    color: "white",
    cursor: "pointer",
    fontWeight: "500",
  },

  googleButton: {
    padding: "12px",
    borderRadius: "8px",
    border: "1px solid #ddd",
    backgroundColor: "white",
    cursor: "pointer",
  },

  divider: {
    textAlign: "center",
    fontSize: "12px",
    color: "#999",
  },

  toggleText: {
    fontSize: "14px",
    textAlign: "center",
  },

  link: {
    color: "#2563eb",
    cursor: "pointer",
    fontWeight: "500",
  },

  eyeButton: {
    position: "absolute",
    right: "10px",
    top: "9px",
    background: "transparent",
    border: "none",
    cursor: "pointer",
    fontSize: "16px",
  },
};