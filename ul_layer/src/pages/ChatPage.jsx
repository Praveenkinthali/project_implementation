import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import ChatWindow from "../features/chat/ChatWindow";
import ChatInput from "../features/chat/ChatInput";
import EvaluationPanel from "../features/chat/EvaluationPanel";
import Sidebar from "../shared/components/Sidebar";
import api from "../api/axiosConfig";

export default function ChatPage() {

  const navigate = useNavigate();
  const user = localStorage.getItem("user_email");

  const [conversations, setConversations] = useState(() => {
    const saved = localStorage.getItem(`srpp_chats_${user}`);
    return saved ? JSON.parse(saved) : [];
  });

  const [activeId, setActiveId] = useState(null);
  const [evaluation, setEvaluation] = useState(null);
  const [loading, setLoading] = useState(false);

  /* SAVE CHAT HISTORY */

  useEffect(() => {
    localStorage.setItem(
      `srpp_chats_${user}`,
      JSON.stringify(conversations)
    );
  }, [conversations, user]);

  /* INITIAL CHAT */

  useEffect(() => {

    if (conversations.length === 0) {

      const firstChat = {
        id: Date.now(),
        title: "New Chat",
        messages: [],
      };

      setConversations([firstChat]);
      setActiveId(firstChat.id);

    } else if (!activeId) {

      setActiveId(conversations[0].id);

    }

  }, []);

  const activeConversation =
    conversations.find((c) => c.id === activeId) || null;

  /* CREATE NEW CHAT */

  const handleNewChat = () => {

    const existingEmpty = conversations.find(
      (chat) => chat.messages.length === 0
    );

    if (existingEmpty) {
      setActiveId(existingEmpty.id);
      return;
    }

    const newChat = {
      id: Date.now(),
      title: "New Chat",
      messages: [],
    };

    setConversations((prev) => [newChat, ...prev]);
    setActiveId(newChat.id);
    setEvaluation(null);

  };

  /* DELETE CHAT */

  const handleDeleteChat = (chatId) => {

    const updated = conversations.filter(
      (c) => c.id !== chatId
    );

    setConversations(updated);

    if (updated.length > 0) {
      setActiveId(updated[0].id);
    } else {
      handleNewChat();
    }

  };

  /* SEND PROMPT */

  const handleSend = async (text) => {

    if (!activeId) return;

    setLoading(true);

    /* ADD USER MESSAGE */

    setConversations((prev) =>
      prev.map((c) =>
        c.id === activeId
          ? {
              ...c,
              title:
                c.messages.length === 0
                  ? text.slice(0, 35)
                  : c.title,
              messages: [
                ...c.messages,
                { role: "user", content: text },
              ],
            }
          : c
      )
    );

    try {

      const response = await api.post("/optimize", {
        prompt: text,
      });

      const data = response.data;

      /* ADD ASSISTANT RESPONSE */

      setConversations((prev) =>
        prev.map((c) =>
          c.id === activeId
            ? {
                ...c,
                messages: [
                  ...c.messages,
                  {
                    role: "assistant",
                    content: data.optimized_prompt,
                  },
                ],
              }
            : c
        )
      );

      setEvaluation({
        final_score: data.final_score,
        should_iterate: data.should_iterate,
      });

    } catch (error) {

      console.error("Backend error:", error);

    }

    setLoading(false);

  };

  /* REGENERATE RESPONSE IN PLACE */

  const handleRegenerate = async () => {

    if (!activeConversation) return;

    const lastUserMessage =
      [...activeConversation.messages]
        .reverse()
        .find((m) => m.role === "user");

    if (!lastUserMessage) return;

    setLoading(true);

    try {

      const res = await api.post("/optimize", {
        prompt: lastUserMessage.content,
      });

      const data = res.data;

      setConversations((prev) =>
        prev.map((chat) => {

          if (chat.id !== activeId) return chat;

          const updatedMessages = [...chat.messages];

          /* REMOVE LAST ASSISTANT RESPONSE */

          if (
            updatedMessages.length &&
            updatedMessages[updatedMessages.length - 1].role === "assistant"
          ) {
            updatedMessages.pop();
          }

          /* INSERT NEW RESPONSE */

          updatedMessages.push({
            role: "assistant",
            content: data.optimized_prompt,
          });

          return {
            ...chat,
            messages: updatedMessages,
          };

        })
      );

      setEvaluation({
        final_score: data.final_score,
        should_iterate: data.should_iterate,
      });

    } catch (err) {

      console.error("Regenerate error:", err);

    }

    setLoading(false);

  };

  /* A/B TEST NAVIGATION */

  const handleABTest = () => {

    if (!activeConversation) return;

    const originalPrompt =
      activeConversation.messages.find(
        (m) => m.role === "user"
      )?.content;

    const optimizedPrompt =
      activeConversation.messages.find(
        (m) => m.role === "assistant"
      )?.content;

    navigate("/ab-testing", {
      state: { originalPrompt, optimizedPrompt },
    });

  };

  return (

    <div style={{ display: "flex", flex: 1 }}>

      <Sidebar
        conversations={conversations}
        activeId={activeId}
        onSelect={setActiveId}
        onNewChat={handleNewChat}
        onDeleteChat={handleDeleteChat}
      />

      <div style={{ flex: 1, display: "flex" }}>

        <div
          style={{
            flex: 1,
            display: "flex",
            flexDirection: "column",
          }}
        >

          <ChatWindow
            messages={activeConversation?.messages || []}
            loading={loading}
            onABTest={handleABTest}
            onRegenerate={handleRegenerate}
          />

          <ChatInput onSend={handleSend} />

        </div>

        <EvaluationPanel evaluation={evaluation} />

      </div>

    </div>

  );
}