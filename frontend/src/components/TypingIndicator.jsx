function TypingIndicator() {
  return (
    <div className="flex justify-start mb-6">
      <div className="max-w-[80%]">

        <p className="text-sm mb-2 font-semibold text-green-400">
          EPC RAG Assistant
        </p>

        <div className="bg-slate-800 border border-slate-700 rounded-2xl px-5 py-4 shadow-lg">

          <div className="flex items-center gap-2">

            <span
              className="w-2 h-2 rounded-full bg-gray-300 animate-bounce"
              style={{ animationDelay: "0ms" }}
            ></span>

            <span
              className="w-2 h-2 rounded-full bg-gray-300 animate-bounce"
              style={{ animationDelay: "150ms" }}
            ></span>

            <span
              className="w-2 h-2 rounded-full bg-gray-300 animate-bounce"
              style={{ animationDelay: "300ms" }}
            ></span>

            <span className="ml-3 text-gray-400 text-sm">
              Thinking...
            </span>

          </div>

        </div>

      </div>
    </div>
  );
}

export default TypingIndicator;