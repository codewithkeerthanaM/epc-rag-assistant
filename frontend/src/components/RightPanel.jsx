import RagasCard from "./RagasCard";

function RightPanel({
  sources = [],
  chunks = [],
  liveEvaluation = null,

  // Runtime RAGAS
  lastQuestion,
  lastAnswer,
  lastContext,
}) {
  const safeSources = Array.isArray(sources) ? sources : [];
  const safeChunks = Array.isArray(chunks) ? chunks : [];

  return (
    <aside className="w-80 bg-slate-800 border-l border-slate-700 p-6 overflow-y-auto">

      {/* ========================================= */}
      {/* Live Answer Evaluation */}
      {/* ========================================= */}

      <h2 className="text-lg font-semibold mb-4">
        🟢 Live Answer Evaluation
      </h2>

      <div className="bg-slate-900 rounded-lg p-4 mb-6">

        {liveEvaluation ? (

          <div className="space-y-4">

            <div>
              <p className="text-xs text-slate-400">
                Overall Status
              </p>

              <p className="text-green-400 font-semibold">
                {liveEvaluation.overall_status}
              </p>
            </div>

            <div>
              <p className="text-xs text-slate-400">
                Confidence
              </p>

              <p className="font-semibold">
                {liveEvaluation.confidence.confidence}
                {" "}
                (
                {liveEvaluation.confidence.confidence_score}
                %)
              </p>
            </div>

            <div>
              <p className="text-xs text-slate-400">
                Retrieval Quality
              </p>

              <p>
                {liveEvaluation.confidence.retrieval_quality}
              </p>
            </div>

            <div>
              <p className="text-xs text-slate-400">
                Evidence Strength
              </p>

              <p>
                {liveEvaluation.evidence.evidence_strength}
              </p>
            </div>

            <div>
              <p className="text-xs text-slate-400">
                Supporting Sources
              </p>

              <p>
                {liveEvaluation.evidence.source_count}
              </p>
            </div>

            <div>
              <p className="text-xs text-slate-400">
                Retrieved Chunks
              </p>

              <p>
                {liveEvaluation.evidence.retrieved_chunks}
              </p>
            </div>

            <div>
              <p className="text-xs text-slate-400">
                Reason
              </p>

              <p className="text-sm text-gray-300">
                {liveEvaluation.confidence.reason}
              </p>
            </div>

          </div>

        ) : (

          <p className="text-sm text-slate-400">
            Ask a question to view the live evaluation.
          </p>

        )}

      </div>

      {/* ========================================= */}
      {/* Source Documents */}
      {/* ========================================= */}

      <h2 className="text-lg font-semibold mb-4">
        📄 Source Documents
      </h2>

      <div className="bg-slate-900 rounded-lg p-4 mb-6">

        {safeSources.length > 0 ? (

          <ul className="space-y-2">

            {safeSources.map((source, index) => (

              <li
                key={index}
                className="text-sm text-green-400 break-words"
              >
                • {source}
              </li>

            ))}

          </ul>

        ) : (

          <p className="text-sm text-slate-400">
            Ask a question to view the retrieved source documents.
          </p>

        )}

      </div>

      {/* ========================================= */}
      {/* Retrieved Chunks */}
      {/* ========================================= */}

      <h2 className="text-lg font-semibold mb-4">
        🧩 Retrieved Chunks
      </h2>

      <div className="bg-slate-900 rounded-lg p-4 mb-6">

        {safeChunks.length > 0 ? (

          <div className="space-y-4">

            {safeChunks.map((chunk, index) => (

              <div
                key={index}
                className="border border-slate-700 rounded-lg p-3"
              >
                <p className="text-xs text-blue-400 mb-2">
                  Chunk {index + 1}
                </p>

                <p className="text-sm text-gray-300 whitespace-pre-wrap">
                  {typeof chunk === "string"
                    ? chunk
                    : JSON.stringify(chunk, null, 2)}
                </p>

              </div>

            ))}

          </div>

        ) : (

          <p className="text-sm text-slate-400">
            Retrieved chunks will appear here after each response.
          </p>

        )}

      </div>

      {/* ========================================= */}
      {/* Runtime RAGAS */}
      {/* ========================================= */}

      <RagasCard
        lastQuestion={lastQuestion}
        lastAnswer={lastAnswer}
        lastContext={lastContext}
      />

    </aside>
  );
}

export default RightPanel;