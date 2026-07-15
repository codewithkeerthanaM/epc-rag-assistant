function StatsBar({
  retrievalScore,
  responseTime,
}) {

  return (
    <footer className="h-16 bg-slate-800 border-t border-slate-700 flex items-center justify-evenly">

      <div className="text-center">
        <p className="text-xs text-slate-400">
          Retrieval Score
        </p>

        <p className="font-semibold text-green-400">
          {retrievalScore !== null
            ? retrievalScore.toFixed(3)
            : "--"}
        </p>
      </div>

      <div className="text-center">
        <p className="text-xs text-slate-400">
          Response Time
        </p>

        <p className="font-semibold text-cyan-400">
          {responseTime
            ? `${responseTime} s`
            : "--"}
        </p>
      </div>

      <div className="text-center">
        <p className="text-xs text-slate-400">
          Model
        </p>

        <p className="font-semibold text-blue-400">
          llama3.1:8b
        </p>
      </div>

      <div className="text-center">
        <p className="text-xs text-slate-400">
          Tokens
        </p>

        <p className="font-semibold text-yellow-400">
          --
        </p>
      </div>

    </footer>
  );
}

export default StatsBar;