import { useState, useEffect } from "react";
import {
  Copy,
  ThumbsUp,
  ThumbsDown,
  RefreshCw,
  MoreHorizontal,
  Check
} from "lucide-react";

export default function ChatWindow({
  messages = [],
  loading,
  onRegenerate,
  onABTest
}) {

  const [liked, setLiked] = useState({});
  const [disliked, setDisliked] = useState({});
  const [copied, setCopied] = useState(null);
  const [showAB, setShowAB] = useState(false);

  const handleCopy = (text, index) => {
    navigator.clipboard.writeText(text);
    setCopied(index);
    setTimeout(() => setCopied(null), 2000);
  };

  const handleLike = (index) => {
    setLiked(prev => ({ ...prev, [index]: !prev[index] }));
    setDisliked(prev => ({ ...prev, [index]: false }));
  };

  const handleDislike = (index) => {
    setDisliked(prev => ({ ...prev, [index]: !prev[index] }));
    setLiked(prev => ({ ...prev, [index]: false }));
  };

  /* SHOW AB BUTTON WHEN RESPONSE ARRIVES */

  useEffect(() => {

    if (!messages.length) return;

    const last = messages[messages.length - 1];

    if (last.role === "assistant") {

      setShowAB(true);

      const timer = setTimeout(() => {
        setShowAB(false);
      }, 4000);

      return () => clearTimeout(timer);
    }

  }, [messages]);

  return (
    <div style={styles.container}>

      {messages.length === 0 && (
        <div style={styles.placeholder}>
          Start a conversation...
        </div>
      )}

      {messages.map((msg, index) => {

        const isUser = msg.role === "user";
        const isAssistant = msg.role === "assistant";
        const isLastAssistant =
          isAssistant && index === messages.length - 1;

        return (

          <div
            key={index}
            style={{
              ...styles.row,
              justifyContent: isUser
                ? "flex-end"
                : "flex-start",
            }}
          >

            <div
              style={styles.block}
              onMouseEnter={() => setShowAB(true)}
              onMouseLeave={() => setShowAB(false)}
            >

              <div
                style={{
                  ...styles.message,
                  background: isUser
                    ? "#2563eb"
                    : "#f3f4f6",
                  color: isUser ? "white" : "black",
                }}
              >
                {msg.content}
              </div>

              {/* A/B BUTTON ABOVE FEEDBACK */}

              {showAB && isLastAssistant && (
                <button
                  style={styles.abButton}
                  onClick={onABTest}
                >
                  Compare Prompts (A/B)
                </button>
              )}

              {/* FEEDBACK TOOLBAR */}

              {isAssistant && (
                <div style={styles.toolbar}>

                  <button
                    style={styles.iconBtn}
                    onClick={() =>
                      handleCopy(msg.content, index)
                    }
                  >
                    {copied === index
                      ? <Check size={16}/>
                      : <Copy size={16}/>
                    }
                  </button>

                  <button
                    style={{
                      ...styles.iconBtn,
                      color: liked[index]
                        ? "#2563eb"
                        : "#666",
                    }}
                    onClick={() => handleLike(index)}
                  >
                    <ThumbsUp size={16}/>
                  </button>

                  <button
                    style={{
                      ...styles.iconBtn,
                      color: disliked[index]
                        ? "#ef4444"
                        : "#666",
                    }}
                    onClick={() => handleDislike(index)}
                  >
                    <ThumbsDown size={16}/>
                  </button>

                  {isLastAssistant && (
                    <button
                      style={styles.iconBtn}
                      onClick={onRegenerate}
                    >
                      <RefreshCw size={16}/>
                    </button>
                  )}

                  <button style={styles.iconBtn}>
                    <MoreHorizontal size={16}/>
                  </button>

                </div>
              )}

            </div>

          </div>
        );
      })}

      {loading && (
        <div style={styles.loading}>
          Generating response...
        </div>
      )}

    </div>
  );
}

const styles = {

  container: {
    flex: 1,
    padding: "25px",
    overflowY: "auto",
    display: "flex",
    flexDirection: "column",
  },

  placeholder: {
    textAlign: "center",
    color: "#888",
    marginTop: "40px",
  },

  row: {
    display: "flex",
    marginBottom: "18px",
  },

  block: {
    maxWidth: "70%",
  },

  message: {
    padding: "12px",
    borderRadius: "8px",
    lineHeight: "1.6",
  },

  abButton: {
    marginTop: "8px",
    padding: "6px 12px",
    borderRadius: "6px",
    border: "1px solid #ddd",
    background: "#f9fafb",
    cursor: "pointer",
    fontSize: "13px",
    alignSelf: "flex-start"
  },

  toolbar: {
    display: "flex",
    gap: "10px",
    marginTop: "6px",
  },

  iconBtn: {
    border: "none",
    background: "transparent",
    cursor: "pointer",
    color: "#666",
    padding: "4px",
  },

  loading: {
    marginTop: "10px",
    color: "#666",
  },

};