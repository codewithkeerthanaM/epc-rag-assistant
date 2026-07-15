import {
  BrowserRouter,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";

import Chat from "./pages/Chat";
import About from "./pages/About";

function App() {
  return (
    <BrowserRouter>

      <div className="h-screen bg-slate-900 text-white">

        <Routes>

          {/* Default Route */}

          <Route
            path="/"
            element={<Navigate to="/chat" replace />}
          />

          {/* Pages */}

          <Route
            path="/chat"
            element={<Chat />}
          />

          <Route
            path="/about"
            element={<About />}
          />

          {/* Unknown Routes */}

          <Route
            path="*"
            element={<Navigate to="/chat" replace />}
          />

        </Routes>

      </div>

    </BrowserRouter>
  );
}

export default App;