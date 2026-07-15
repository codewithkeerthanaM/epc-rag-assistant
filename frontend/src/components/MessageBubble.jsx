import { useState } from "react";
import { FaCopy, FaCheck } from "react-icons/fa";

function MessageBubble({ message }) {
  const isUser = message.role === "user";

  const [copied, setCopied] = useState(false);

  const copyMessage = async () => {
    try {
      await navigator.clipboard.writeText(message.content);
      setCopied(true);

      setTimeout(() => {
        setCopied(false);
      }, 2000);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div
      className={`flex mb-6 ${
        isUser ? "justify-end" : "justify-start"
      }`}
    >
      <div className="max-w-[80%]">

        <div className="flex items-center justify-between mb-2">

          <p
            className={`text-sm font-semibold ${
              isUser
                ? "text-blue-400"
                : "text-green-400"
            }`}
          >
            {isUser ? "You" : "EPC RAG Assistant"}
          </p>

          {!isUser && (
            <button
              onClick={copyMessage}
              className="flex items-center gap-2 text-xs text-slate-400 hover:text-white transition"
            >
              {copied ? (
                <>
                  <FaCheck />
                  Copied
                </>
              ) : (
                <>
                  <FaCopy />
                  Copy
                </>
              )}
            </button>
          )}

        </div>

        <div
          className={`rounded-2xl px-5 py-4 shadow-lg border break-words whitespace-pre-wrap leading-7 ${
            isUser
              ? "bg-blue-600 border-blue-500 text-white"
              : "bg-slate-800 border-slate-700 text-gray-100"
          }`}
        >
          {message.content}
        </div>

      </div>
    </div>
  );
}

export default MessageBubble;