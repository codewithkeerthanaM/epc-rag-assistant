import { createContext, useContext, useState } from "react";

const ChatContext = createContext();

export function ChatProvider({ children }) {

  // Chat Messages
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content:
        "Welcome to the EPC RAG Assistant! Ask me anything about Engineering, Procurement, Construction, Safety, Contracts, or Project Management.",
    },
  ]);

  // Stats
  const [retrievalScore, setRetrievalScore] = useState(null);
  const [responseTime, setResponseTime] = useState(null);

  // Sources & Context
  const [sources, setSources] = useState([]);
  const [chunks, setChunks] = useState([]);

  // Live Evaluation
  const [liveEvaluation, setLiveEvaluation] = useState(null);

  // Runtime Evaluation
  const [lastQuestion, setLastQuestion] = useState(null);
  const [lastAnswer, setLastAnswer] = useState(null);
  const [lastContext, setLastContext] = useState(null);

  // Uploaded PDF
  const [attachedFile, setAttachedFile] = useState(null);

  return (
    <ChatContext.Provider
      value={{
        messages,
        setMessages,

        retrievalScore,
        setRetrievalScore,

        responseTime,
        setResponseTime,

        sources,
        setSources,

        chunks,
        setChunks,

        liveEvaluation,
        setLiveEvaluation,

        lastQuestion,
        setLastQuestion,

        lastAnswer,
        setLastAnswer,

        lastContext,
        setLastContext,

        attachedFile,
        setAttachedFile,
      }}
    >
      {children}
    </ChatContext.Provider>
  );
}

export function useChat() {
  return useContext(ChatContext);
}