import { useState } from "react";

export default function ChatInput({ onSend }) {
  const [input, setInput] = useState("");

  const handleSend = () => {
    if (!input.trim()) return;
    onSend(input);
    setInput("");
  };

  return (
    <div style={styles.inputBar}>
      <input
        type="text"
        placeholder="Send a message..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
        style={styles.input}
      />
      <button onClick={handleSend} style={styles.button}>
        Send
      </button>
    </div>
  );
}

const styles = {
  inputBar: {
    display: "flex",
    padding: "20px",
    borderTop: "1px solid #ddd",
    backgroundColor: "white",
  },

  input: {
    flex: 1,
    padding: "14px",
    borderRadius: "12px",
    border: "1px solid #ccc",
  },

  button: {
    marginLeft: "10px",
    padding: "14px 18px",
    borderRadius: "12px",
    border: "none",
    backgroundColor: "#2563eb",
    color: "white",
    cursor: "pointer",
  },
};