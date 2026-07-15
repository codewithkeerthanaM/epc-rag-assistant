import {
  FaComments,
  FaInfoCircle,
  FaMoon,
} from "react-icons/fa";

import { NavLink } from "react-router-dom";

const menuItems = [
  {
    name: "Chat",
    path: "/chat",
    icon: <FaComments />,
  },
  {
    name: "About",
    path: "/about",
    icon: <FaInfoCircle />,
  },
];

function Sidebar() {
  return (
    <aside className="w-64 flex-shrink-0 bg-slate-800 border-r border-slate-700 flex flex-col">

      {/* Logo */}

      <div className="p-6 border-b border-slate-700">

        <h1 className="text-2xl font-bold">
          EPC RAG
        </h1>

        <p className="text-sm text-slate-400 mt-1">
          Enterprise AI Assistant
        </p>

      </div>

      {/* Navigation */}

      <nav className="flex-1 p-4 space-y-2">

        {menuItems.map((item) => (

          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 ${
                isActive
                  ? "bg-blue-600 text-white shadow-lg"
                  : "text-slate-300 hover:bg-slate-700 hover:text-white"
              }`
            }
          >
            <span className="text-lg">
              {item.icon}
            </span>

            <span>
              {item.name}
            </span>

          </NavLink>

        ))}

      </nav>

      {/* Footer */}

      <div className="border-t border-slate-700 p-4">

        <button className="flex items-center gap-3 w-full px-4 py-3 rounded-xl text-slate-300 hover:bg-slate-700 hover:text-yellow-300 transition-all">

          <FaMoon />

          <span>
            Dark Mode
          </span>

        </button>

        <p className="text-xs text-slate-500 mt-4 text-center">
          Version 1.0
        </p>

      </div>

    </aside>
  );
}

export default Sidebar;