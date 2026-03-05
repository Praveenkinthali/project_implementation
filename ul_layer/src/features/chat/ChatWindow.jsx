import { useState } from "react";
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
}) {

  const [liked, setLiked] = useState({});
  const [disliked, setDisliked] = useState({});
  const [copied, setCopied] = useState(null);

  const handleCopy = (text, index) => {

    navigator.clipboard.writeText(text);

    setCopied(index);

    setTimeout(() => {
      setCopied(null);
    }, 2000);
  };

  const handleLike = (index) => {

    setLiked((prev) => ({
      ...prev,
      [index]: !prev[index]
    }));

    setDisliked((prev) => ({
      ...prev,
      [index]: false
    }));
  };

  const handleDislike = (index) => {

    setDisliked((prev) => ({
      ...prev,
      [index]: !prev[index]
    }));

    setLiked((prev) => ({
      ...prev,
      [index]: false
    }));
  };

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

            <div style={styles.block}>

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

              {isAssistant && (
                <div style={styles.toolbar}>

                  {/* COPY */}

                  <button
                    style={styles.iconBtn}
                    onClick={() =>
                      handleCopy(msg.content, index)
                    }
                  >
                    {copied === index
                      ? <Check size={16} />
                      : <Copy size={16} />
                    }
                  </button>

                  {/* LIKE */}

                  <button
                    style={{
                      ...styles.iconBtn,
                      color: liked[index]
                        ? "#2563eb"
                        : "#666",
                    }}
                    onClick={() => handleLike(index)}
                  >
                    <ThumbsUp size={16} />
                  </button>

                  {/* DISLIKE */}

                  <button
                    style={{
                      ...styles.iconBtn,
                      color: disliked[index]
                        ? "#ef4444"
                        : "#666",
                    }}
                    onClick={() => handleDislike(index)}
                  >
                    <ThumbsDown size={16} />
                  </button>

                  {/* REGENERATE */}

                  {isLastAssistant && (
                    <button
                      style={styles.iconBtn}
                      onClick={onRegenerate}
                    >
                      <RefreshCw size={16} />
                    </button>
                  )}

                  <button style={styles.iconBtn}>
                    <MoreHorizontal size={16} />
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