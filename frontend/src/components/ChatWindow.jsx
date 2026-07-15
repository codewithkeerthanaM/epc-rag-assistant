import { useState, useRef, useEffect } from "react";
import MessageBubble from "./MessageBubble";
import ChatInput from "./ChatInput";
import TypingIndicator from "./TypingIndicator";
import api from "../services/api";

import { useChat } from "../context/ChatContext";

function ChatWindow() {

  const {

    messages,
    setMessages,

    attachedFile,
    setAttachedFile,

    setRetrievalScore,
    setResponseTime,

    setSources,
    setChunks,

    setLiveEvaluation,

    setLastQuestion,
    setLastAnswer,
    setLastContext,

  } = useChat();

  const [loading, setLoading] = useState(false);

  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading]);

  const handleSend = async (text) => {

    if (!text.trim()) return;

    setMessages(prev => [
      ...prev,
      {
        role: "user",
        content: text,
      },
    ]);

    setLoading(true);

    const startTime = performance.now();

    try {

      const response = await api.post("/ask", {

        question: text,

        use_uploaded_document: attachedFile !== null,

      });

      const endTime = performance.now();

      setResponseTime(
        ((endTime - startTime) / 1000).toFixed(2)
      );

      setRetrievalScore(
        response.data.retrieval_score ?? null
      );

      const src =
        Array.isArray(response.data.sources)
          ? response.data.sources
          : [];

      setSources(src);

      let contextData = [];

      if (Array.isArray(response.data.context)) {
        contextData = response.data.context;
      } else if (
        typeof response.data.context === "string"
      ) {
        contextData = [response.data.context];
      }

      setChunks(contextData);

      setLiveEvaluation(
        response.data.live_evaluation ?? null
      );

      setLastQuestion(text);

      setLastAnswer(
        response.data.answer ??
          "No answer received."
      );

      setLastContext(contextData);

      setMessages(prev => [
        ...prev,
        {
          role: "assistant",
          content:
            response.data.answer ??
            "No answer received.",
        },
      ]);

    } catch (error) {

      console.error(error);

      setMessages(prev => [
        ...prev,
        {
          role: "assistant",
          content:
            "❌ Unable to connect to backend.",
        },
      ]);

    } finally {

      setLoading(false);

    }

  };

  return (

    <div className="flex flex-col flex-1 min-h-0 bg-slate-900">

      <div className="flex-1 min-h-0 overflow-y-auto">

        <div className="max-w-4xl mx-auto p-8">

          {messages.map((msg, index) => (

            <MessageBubble
              key={index}
              message={msg}
            />

          ))}

          {loading && <TypingIndicator />}

          <div ref={messagesEndRef} />

        </div>

      </div>

      <div className="border-t border-slate-700 bg-slate-900 p-6 flex-shrink-0">

        <div className="max-w-4xl mx-auto">

          <ChatInput
            onSend={handleSend}
            loading={loading}
            attachedFile={attachedFile}
            setAttachedFile={setAttachedFile}
          />

        </div>

      </div>

    </div>

  );

}

export default ChatWindow;