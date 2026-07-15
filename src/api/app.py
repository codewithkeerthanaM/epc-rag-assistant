from pathlib import Path
import shutil
import pandas as pd

from fastapi import (
    FastAPI,
    UploadFile,
    File,
    Form,
    HTTPException,
)
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.chat.upload_manager import save_uploaded_pdf
from src.chat.temp_document_processor import process_uploaded_pdf
from src.chat.temporary_engine import (
    answer_question as temporary_answer_question,
)

from src.reasoning.rag_engine import (
    answer_question,
    conversation_history,
)

from src.live_evaluation.evaluator import evaluate_response

# NEW
from src.ragas_runtime.single_answer import evaluate_single_answer

app = FastAPI(
    title="EPC RAG API",
    version="2.0",
)

# ----------------------------------------------------
# CORS
# ----------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------------------------
# Constants
# ----------------------------------------------------

RAW_DATA_DIR = Path("data/raw")

# ----------------------------------------------------
# Models
# ----------------------------------------------------

class QuestionRequest(BaseModel):
    question: str
    use_uploaded_document: bool = False


# NEW
class EvaluateRequest(BaseModel):
    question: str
    answer: str
    context: str | list


# ----------------------------------------------------
# Home
# ----------------------------------------------------

@app.get("/")
def home():

    return {
        "message": "EPC Multimodal RAG API Running"
    }


# ----------------------------------------------------
# Evaluation Results
# ----------------------------------------------------

@app.get("/evaluation")
def get_evaluation():

    report_path = Path("data/evaluation/ragas_report.csv")

    if not report_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Evaluation report not found."
        )

    df = pd.read_csv(report_path)

    rows = df.to_dict(orient="records")

    for row in rows:
        for key, value in row.items():
            if pd.isna(value):
                row[key] = None

    return {
        "success": True,
        "rows": rows,
        "total_questions": len(rows)
    }


# ----------------------------------------------------
# Runtime RAGAS Evaluation
# ----------------------------------------------------

@app.post("/evaluate-answer")
def evaluate_runtime_answer(request: EvaluateRequest):

    return evaluate_single_answer(

        question=request.question,

        answer=request.answer,

        context=request.context,

    )


# ----------------------------------------------------
# Ask Question
# ----------------------------------------------------

@app.post("/ask")
def ask_question(request: QuestionRequest):

    """
    Smart routing:

    1. Uploaded PDF
    2. Permanent EPC Knowledge Base

    Then perform Live Answer Evaluation.
    """

    if request.use_uploaded_document:

        result = temporary_answer_question(
            request.question
        )

    else:

        result = answer_question(
            request.question
        )

    result["live_evaluation"] = evaluate_response(

        retrieval_score=result.get(
            "retrieval_score"
        ),

        sources=result.get(
            "sources",
            [],
        ),

        retrieved_context=result.get(
            "context",
            "",
        ),

    )

    return result


# ----------------------------------------------------
# Reset Permanent Conversation Memory
# ----------------------------------------------------

@app.post("/reset-memory")
def reset_memory():

    conversation_history.clear()

    return {

        "message": "Conversation memory cleared."

    }


# =====================================================
# Temporary Chat Upload
# =====================================================

@app.post("/chat/upload")
async def upload_chat_pdf(
    file: UploadFile = File(...)
):

    try:

        pdf_path = save_uploaded_pdf(file)

        result = process_uploaded_pdf(pdf_path)

        return {

            "success": True,

            "filename": result["filename"],

            "chunks": result["chunks"],

            "message": "Temporary document indexed successfully."

        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =====================================================
# Temporary Chat
# =====================================================

@app.post("/chat/ask")
def chat_with_uploaded_document(
    request: QuestionRequest
):

    try:

        result = temporary_answer_question(
            request.question
        )

        return result

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =====================================================
# Permanent Knowledge Base Upload
# =====================================================

@app.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...),
    category: str = Form(...),
):

    allowed_categories = [

        "engineering",

        "procurement",

        "construction",

        "project_management",

        "safety",

    ]

    category = category.lower()

    if category not in allowed_categories:

        raise HTTPException(
            status_code=400,
            detail="Invalid category."
        )

    if not file.filename.lower().endswith(".pdf"):

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    save_directory = RAW_DATA_DIR / category

    save_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    destination = save_directory / file.filename

    with destination.open("wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer,
        )

    return {

        "success": True,

        "filename": file.filename,

        "category": category,

        "message": "PDF uploaded successfully."

    }