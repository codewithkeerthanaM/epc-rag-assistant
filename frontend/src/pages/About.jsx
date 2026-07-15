import DashboardLayout from "../layouts/DashboardLayout";

function About() {
  const technologies = [
    "React",
    "Vite",
    "FastAPI",
    "Python",
    "FAISS",
    "Sentence Transformers",
    "Ollama",
    "Llama 3.1",
    "RAGAS",
    "PyPDF",
  ];

  const features = [
    "AI-powered EPC Question Answering",
    "Semantic Document Search",
    "PDF Upload & Chat",
    "Conversation Memory",
    "Source Citation",
    "Knowledge Base Search",
    "RAGAS Evaluation",
    "Retrieval Score",
  ];

  const domains = [
    "Engineering",
    "Procurement",
    "Construction",
    "Safety",
    "Project Management",
  ];

  return (
    <DashboardLayout>
      <div className="p-10 space-y-8 text-white overflow-y-auto h-full">

        {/* Hero Section */}
        <div className="bg-slate-800 border border-slate-700 rounded-2xl p-8">
          <h1 className="text-4xl font-bold text-blue-400">
            EPC RAG Assistant
          </h1>

          <p className="mt-6 text-slate-300 leading-8 text-lg">
            EPC RAG Assistant is a domain-specific AI application developed to
            provide intelligent question answering from Engineering,
            Procurement and Construction (EPC) documents. It combines
            Retrieval-Augmented Generation (RAG), semantic search, vector
            databases and Large Language Models to deliver accurate,
            context-aware answers with source references.
          </p>
        </div>

        {/* Project Overview */}
        <div className="bg-slate-800 border border-slate-700 rounded-2xl p-8">
          <h2 className="text-2xl font-semibold text-blue-400 mb-4">
            Project Overview
          </h2>

          <p className="text-slate-300 leading-8">
            The project allows users to upload EPC-related PDF documents and
            ask questions in natural language. Documents are converted into
            embeddings, stored in a FAISS vector database and retrieved using
            semantic similarity search. Retrieved content is reranked and
            provided to the Large Language Model to generate reliable answers.
          </p>
        </div>

        {/* Domains */}
        <div>
          <h2 className="text-2xl font-semibold mb-4">
            Supported Domains
          </h2>

          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            {domains.map((domain) => (
              <div
                key={domain}
                className="bg-slate-800 border border-slate-700 rounded-xl p-5 text-center hover:bg-slate-700 transition"
              >
                {domain}
              </div>
            ))}
          </div>
        </div>

        {/* Features */}
        <div>
          <h2 className="text-2xl font-semibold mb-4">
            Key Features
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {features.map((feature) => (
              <div
                key={feature}
                className="bg-slate-800 border border-slate-700 rounded-xl p-4"
              >
                ✅ {feature}
              </div>
            ))}
          </div>
        </div>

        {/* Statistics */}
        <div>
          <h2 className="text-2xl font-semibold mb-4">
            Project Statistics
          </h2>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-5">

            <div className="bg-slate-800 border border-slate-700 rounded-xl p-5">
              <p className="text-slate-400 text-sm">PDF Documents</p>
              <h3 className="text-2xl font-bold mt-2">113+</h3>
            </div>

            <div className="bg-slate-800 border border-slate-700 rounded-xl p-5">
              <p className="text-slate-400 text-sm">Knowledge Chunks</p>
              <h3 className="text-2xl font-bold mt-2">18,804</h3>
            </div>

            <div className="bg-slate-800 border border-slate-700 rounded-xl p-5">
              <p className="text-slate-400 text-sm">Vector Database</p>
              <h3 className="text-2xl font-bold mt-2">FAISS</h3>
            </div>

            <div className="bg-slate-800 border border-slate-700 rounded-xl p-5">
              <p className="text-slate-400 text-sm">Embedding Model</p>
              <h3 className="text-2xl font-bold mt-2">
                all-MiniLM-L6-v2
              </h3>
            </div>

          </div>
        </div>

        {/* Technology Stack */}
        <div>
          <h2 className="text-2xl font-semibold mb-4">
            Technology Stack
          </h2>

          <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
            {technologies.map((tech) => (
              <div
                key={tech}
                className="bg-slate-800 border border-slate-700 rounded-xl p-4 text-center hover:bg-slate-700 transition"
              >
                {tech}
              </div>
            ))}
          </div>
        </div>

        {/* Workflow */}
        <div className="bg-slate-800 border border-slate-700 rounded-2xl p-8">
          <h2 className="text-2xl font-semibold text-blue-400 mb-4">
            How It Works
          </h2>

          <ol className="list-decimal list-inside space-y-3 text-slate-300">
            <li>User uploads EPC PDF documents.</li>
            <li>Text is extracted and divided into chunks.</li>
            <li>Embeddings are generated using Sentence Transformers.</li>
            <li>Embeddings are stored in a FAISS vector database.</li>
            <li>Relevant chunks are retrieved through semantic search.</li>
            <li>Retrieved results are reranked for better relevance.</li>
            <li>Llama 3.1 generates an accurate response with sources.</li>
          </ol>
        </div>

        {/* Footer */}
        <div className="bg-slate-800 border border-slate-700 rounded-2xl p-8">
          <h2 className="text-2xl font-bold text-blue-400 mb-4">
            About the Project
          </h2>

          <p className="text-slate-300 leading-8">
            This project was developed as part of an AI internship to build a
            domain-specific Retrieval-Augmented Generation system for the EPC
            industry. By integrating React, FastAPI, FAISS, Sentence
            Transformers, Ollama and Llama 3.1, the application delivers fast,
            accurate and explainable answers from engineering documents while
            improving retrieval quality through RAGAS evaluation.
          </p>
        </div>

      </div>
    </DashboardLayout>
  );
}

export default About;