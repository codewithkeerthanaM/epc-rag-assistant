import React from "react";
import ReactDOM from "react-dom/client";

import App from "./App";
import "./index.css";

import { ChatProvider } from "./context/ChatContext";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <ChatProvider>
      <App />
    </ChatProvider>
  </React.StrictMode>
);