import DashboardLayout from "../layouts/DashboardLayout";

import ChatWindow from "../components/ChatWindow";
import RightPanel from "../components/RightPanel";
import StatsBar from "../components/StatsBar";

import { useChat } from "../context/ChatContext";

function Chat() {

  const {

    retrievalScore,
    setRetrievalScore,

    responseTime,
    setResponseTime,

    sources,
    setSources,

    chunks,
    setChunks,

    liveEvaluation,
    setLiveEvaluation,

    lastQuestion,
    setLastQuestion,

    lastAnswer,
    setLastAnswer,

    lastContext,
    setLastContext,

  } = useChat();

  return (

    <DashboardLayout>

      <div className="flex h-full">

        <div className="flex flex-col flex-1 min-w-0">

          <ChatWindow
            setRetrievalScore={setRetrievalScore}
            setResponseTime={setResponseTime}
            setSources={setSources}
            setChunks={setChunks}
            setLiveEvaluation={setLiveEvaluation}
            setLastQuestion={setLastQuestion}
            setLastAnswer={setLastAnswer}
            setLastContext={setLastContext}
          />

          <StatsBar
            retrievalScore={retrievalScore}
            responseTime={responseTime}
          />

        </div>

        <RightPanel
          sources={sources}
          chunks={chunks}
          liveEvaluation={liveEvaluation}
          lastQuestion={lastQuestion}
          lastAnswer={lastAnswer}
          lastContext={lastContext}
        />

      </div>

    </DashboardLayout>

  );
}

export default Chat;