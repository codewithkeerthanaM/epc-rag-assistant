import Sidebar from "../components/Sidebar";
import TopBar from "../components/TopBar";

function DashboardLayout({ children }) {
  return (
    <div className="flex h-screen bg-slate-900 text-white overflow-hidden">

      <Sidebar />

      <div className="flex flex-col flex-1 min-w-0">

        <TopBar />

        <main className="flex-1 overflow-hidden">
          {children}
        </main>

      </div>

    </div>
  );
}

export default DashboardLayout;