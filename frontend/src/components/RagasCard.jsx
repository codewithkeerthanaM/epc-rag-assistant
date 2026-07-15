import { useState } from "react";
import api from "../services/api";

function RagasCard({
  lastQuestion,
  lastAnswer,
  lastContext,
}) {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const evaluate = async () => {
    if (!lastQuestion || !lastAnswer) return;

    try {
      setLoading(true);
      setResult(null);

      const response = await api.post("/evaluate-answer", {
        question: lastQuestion,
        answer: lastAnswer,
        context: lastContext,
      });

      console.log("Runtime RAGAS Response:");
      console.log(response.data);

      setResult(response.data);

    } catch (err) {
      console.error(err);

      setResult({
        success: false,
        message: "Runtime evaluation failed.",
      });

    } finally {
      setLoading(false);
    }
  };

  const metrics = result?.metrics || {};

  return (
    <div className="bg-slate-900 rounded-lg p-4 mt-6">

      <h2 className="text-lg font-semibold mb-4">
        🧠 Runtime RAGAS
      </h2>

      <button
        onClick={evaluate}
        disabled={loading || !lastQuestion}
        className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-slate-700 rounded-lg py-2 transition"
      >
        {loading ? "Evaluating..." : "Evaluate Answer"}
      </button>

      {result && !result.success && (
        <div className="mt-4 bg-red-900/30 border border-red-500 rounded-lg p-3">
          <p className="text-red-300">
            {result.message}
          </p>
        </div>
      )}

      {result?.success && (

        <div className="mt-5 space-y-3">

          <div>
            <p className="text-sm text-slate-400">Faithfulness</p>
            <p className="font-semibold">
              {metrics.faithfulness ?? "N/A"}
            </p>
          </div>

          <div>
            <p className="text-sm text-slate-400">Answer Relevancy</p>
            <p className="font-semibold">
              {metrics.answer_relevancy ?? "N/A"}
            </p>
          </div>

          <div>
            <p className="text-sm text-slate-400">Context Precision</p>
            <p className="font-semibold">
              {metrics.context_precision ?? "N/A"}
            </p>
          </div>

          <div>
            <p className="text-sm text-slate-400">Context Recall</p>
            <p className="font-semibold">
              {metrics.context_recall ?? "N/A"}
            </p>
          </div>

          <hr className="border-slate-700" />

          <div>
            <p className="text-sm text-slate-400 mb-2">
              Ground Truth
            </p>

            <div className="bg-slate-800 rounded-lg p-3 text-sm whitespace-pre-wrap max-h-60 overflow-y-auto">
              {result.ground_truth}
            </div>
          </div>

        </div>

      )}

    </div>
  );
}

export default RagasCard;