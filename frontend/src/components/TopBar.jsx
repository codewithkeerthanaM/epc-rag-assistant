function TopBar() {
  return (
    <header className="h-16 flex-shrink-0 bg-slate-800 border-b border-slate-700 flex items-center justify-between px-6">

      <div>
        <h1 className="text-xl font-bold">
          Engineering • Procurement • Construction
        </h1>

        <p className="text-sm text-slate-400">
          Enterprise AI Assistant
        </p>
      </div>

      <div className="text-right">
        <p className="text-sm text-slate-400">
          Model
        </p>

        <p className="font-semibold text-blue-400">
          Llama 3.1 : 8B
        </p>
      </div>

    </header>
  );
}

export default TopBar;