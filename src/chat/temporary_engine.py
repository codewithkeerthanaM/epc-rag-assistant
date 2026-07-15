from src.retrieval.temp_retriever import temporary_retriever
import ollama


# --------------------------------------------------
# Temporary Conversation Memory
# --------------------------------------------------

conversation_history = []


# --------------------------------------------------
# Answer Question
# --------------------------------------------------

def answer_question(query):

    global conversation_history

    if not temporary_retriever.has_document():

        return {

            "answer": (
                "No temporary document has been uploaded."
            ),

            "sources": [],

            "retrieval_score": 0.0,

            "context": []

        }

    # ---------------------------------------------
    # History-aware Retrieval
    # ---------------------------------------------

    retrieval_query = query

    if len(conversation_history) > 0:

        last_question = conversation_history[-1]["user"]

        retrieval_query = f"{last_question} {query}"

    # ---------------------------------------------
    # Retrieve Chunks
    # ---------------------------------------------

    retrieved_chunks = temporary_retriever.search(

        retrieval_query,

        top_k=5

    )

    if len(retrieved_chunks) == 0:

        return {

            "answer": "No relevant information found.",

            "sources": [],

            "retrieval_score": 0.0,

            "context": []

        }

    # ---------------------------------------------
    # Build Context
    # ---------------------------------------------

    context = []

    sources = []

    for chunk in retrieved_chunks:

        sources.append(

            f"{chunk['source_file']} (Chunk {chunk['chunk_id']})"

        )

        context.append(

            f"""

Source: {chunk['source_file']}

{chunk['text']}

"""

        )

    # ---------------------------------------------
    # Conversation History
    # ---------------------------------------------

    history_text = ""

    for item in conversation_history:

        history_text += f"""

User: {item['user']}

Assistant: {item['assistant']}

"""

    # ---------------------------------------------
    # Prompt
    # ---------------------------------------------

    prompt = f"""
You are an AI assistant.

Answer ONLY from the uploaded document.

Rules:

1. Use ONLY the provided context.
2. Never invent information.
3. If the answer is unavailable, say:

Information not found in uploaded document.

4. Answer clearly.
5. Use bullet points whenever appropriate.

Conversation History:

{history_text}

Context:

{chr(10).join(context)}

Question:

{query}

Answer:
"""

    # ---------------------------------------------
    # LLM
    # ---------------------------------------------

    response = ollama.chat(

        model="llama3.1:8b",

        messages=[

            {

                "role": "user",

                "content": prompt

            }

        ]

    )

    answer = response["message"]["content"]

    # ---------------------------------------------
    # Update Memory
    # ---------------------------------------------

    conversation_history.append(

        {

            "user": query,

            "assistant": answer

        }

    )

    if len(conversation_history) > 3:

        conversation_history.pop(0)

    # ---------------------------------------------
    # Return
    # ---------------------------------------------

    return {

        "answer": answer,

        "sources": sorted(set(sources)),

        "retrieval_score": 1.0,

        "context": context

    }