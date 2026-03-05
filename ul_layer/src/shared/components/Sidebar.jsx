import { useNavigate } from "react-router-dom";

export default function Sidebar({
  conversations = [],
  activeId,
  onSelect,
  onNewChat,
  onDeleteChat,
}) {
  const navigate = useNavigate();

  return (
    <div style={styles.sidebar}>

      {/* PROJECT NAME */}
      <div style={styles.brand}>
        SRPP Studio
      </div>

      {/* NEW CHAT */}
      <button style={styles.newChat} onClick={onNewChat}>
        + New Chat
      </button>

      {/* CHAT LIST */}
      <div style={styles.chatList}>
        {conversations.map((chat) => (
          <div
            key={chat.id}
            style={{
              ...styles.chatItem,
              backgroundColor:
                activeId === chat.id ? "#2a2b32" : "transparent",
            }}
          >

            <span
              style={styles.chatTitle}
              onClick={() => onSelect(chat.id)}
            >
              {chat.title}
            </span>

            <span
              style={styles.deleteBtn}
              onClick={() => onDeleteChat(chat.id)}
            >
              🗑
            </span>

          </div>
        ))}
      </div>

      {/* PROFILE + SETTINGS */}
      <div style={styles.bottom}>
        <div style={styles.link} onClick={() => navigate("/profile")}>
          Profile
        </div>

        <div style={styles.link} onClick={() => navigate("/settings")}>
          Settings
        </div>
      </div>

    </div>
  );
}

const styles = {

  sidebar: {
    width: "260px",
    backgroundColor: "#202123",
    color: "white",
    display: "flex",
    flexDirection: "column",
    padding: "15px",
  },

  brand: {
    fontSize: "20px",
    fontWeight: "bold",
    marginBottom: "20px",
  },

  newChat: {
    padding: "10px",
    marginBottom: "15px",
    borderRadius: "6px",
    border: "1px solid #444",
    backgroundColor: "#343541",
    color: "white",
    cursor: "pointer",
  },

  chatList: {
    flex: 1,
    overflowY: "auto",
  },

  chatItem: {
    padding: "8px",
    borderRadius: "6px",
    cursor: "pointer",
    marginBottom: "6px",
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
  },

  chatTitle: {
    flex: 1,
  },

  deleteBtn: {
    marginLeft: "8px",
    cursor: "pointer",
    opacity: 0.7,
  },

  bottom: {
    borderTop: "1px solid #444",
    paddingTop: "10px",
    fontSize: "14px",
  },

  link: {
    cursor: "pointer",
    padding: "6px 0",
  },
};