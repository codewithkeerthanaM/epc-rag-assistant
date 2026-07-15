import { useRef, useState } from "react";
import {
  FaPaperPlane,
  FaPaperclip,
  FaTimes,
  FaFilePdf,
} from "react-icons/fa";
import api from "../services/api";

function ChatInput({
  onSend,
  loading,
  attachedFile,
  setAttachedFile,
}) {
  const [text, setText] = useState("");
  const [uploading, setUploading] = useState(false);

  const fileInputRef = useRef(null);

  // -------------------------
  // Send Message
  // -------------------------

  const handleSend = () => {
    if (loading || uploading) return;

    if (!text.trim()) return;

    onSend(text);

    setText("");
  };

  // -------------------------
  // Enter Key
  // -------------------------

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  // -------------------------
  // Upload PDF
  // -------------------------

  const handleFileChange = async (event) => {
    const file = event.target.files[0];

    if (!file) return;

    if (file.type !== "application/pdf") {
      alert("Please select a PDF file.");
      return;
    }

    try {
      setUploading(true);

      const formData = new FormData();
      formData.append("file", file);

      const response = await api.post(
        "/chat/upload",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      console.log("Upload Response:");
      console.log(response.data);

      setAttachedFile(file);
    } catch (error) {
      console.error(error);

      alert("Failed to upload PDF.");

      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }
    } finally {
      setUploading(false);
    }
  };

  // -------------------------
  // Remove PDF
  // -------------------------

  const removeAttachment = () => {
    setAttachedFile(null);

    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }

    /*
      Later we'll also call:

      POST /chat/clear

      which clears the temporary
      vector database.

      Not required yet.
    */
  };

  return (
    <div className="space-y-3">
      {/* Uploaded PDF */}

      {attachedFile && (
        <div className="flex items-center justify-between bg-slate-800 border border-slate-700 rounded-xl px-4 py-3">
          <div className="flex items-center gap-3">
            <FaFilePdf className="text-red-500 text-xl" />

            <div>
              <p className="font-medium">
                {attachedFile.name}
              </p>

              <p className="text-xs text-green-400">
                Ready for chat
              </p>

              <p className="text-xs text-slate-400">
                {(attachedFile.size / 1024 / 1024).toFixed(2)} MB
              </p>
            </div>
          </div>

          <button
            onClick={removeAttachment}
            className="text-slate-400 hover:text-red-400 transition"
          >
            <FaTimes />
          </button>
        </div>
      )}

      {/* Chat Input */}

      <div className="flex items-center gap-3 bg-slate-900 border border-slate-700 rounded-2xl px-3 py-3">
        {/* Hidden Input */}

        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf"
          className="hidden"
          onChange={handleFileChange}
        />

        {/* Paperclip */}

        <button
          onClick={() => fileInputRef.current.click()}
          disabled={loading || uploading}
          className="w-11 h-11 rounded-xl flex items-center justify-center hover:bg-slate-800 transition"
          title="Attach PDF"
        >
          {uploading ? (
            <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
          ) : (
            <FaPaperclip className="text-lg" />
          )}
        </button>

        {/* Text */}

        <input
          type="text"
          value={text}
          disabled={loading || uploading}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={
            attachedFile
              ? "Ask anything about the uploaded PDF..."
              : "Ask anything about Engineering, Procurement or Construction..."
          }
          className="flex-1 bg-transparent outline-none text-white placeholder:text-slate-500"
        />

        {/* Send */}

        <button
          onClick={handleSend}
          disabled={loading || uploading}
          className="w-11 h-11 rounded-xl bg-blue-600 hover:bg-blue-700 disabled:bg-slate-700 transition flex items-center justify-center"
        >
          {loading ? (
            <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
          ) : (
            <FaPaperPlane />
          )}
        </button>
      </div>
    </div>
  );
}

export default ChatInput;