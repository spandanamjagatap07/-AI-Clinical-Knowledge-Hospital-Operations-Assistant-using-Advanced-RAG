
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel

from backend.agents.agent_executor import execute_agent
from backend.rag.sql_analytics import handle_sql_question
from backend.agents.report_generator import generate_incident_report

from backend.auth.router import router as auth_router
from backend.auth.dependencies import get_current_user
from backend.database.models import User
from backend.api.documents import router as documents_router


app = FastAPI(
    title="AI Hospital Assistant API",
    description="REST API for the Enterprise AI Clinical Knowledge and Hospital Operations Assistant",
    version="1.0.0"
)

# Register authentication APIs
app.include_router(auth_router)
app.include_router(documents_router)

class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    question: str
    answer: str


class AnalyticsRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "message": "Welcome to AI Hospital Assistant API",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": "AI Hospital Assistant API"
    }


# Authenticated Chat API
@app.post("/chat", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user)
):
    try:
        if not request.question.strip():
            raise HTTPException(
                status_code=400,
                detail="Question cannot be empty"
            )

        answer = execute_agent(request.question)

        return ChatResponse(
            question=request.question,
            answer=str(answer)
        )

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing the question"
        )


# Authenticated SQL Analytics API
@app.post("/analytics")
def analytics(
    request: AnalyticsRequest,
    current_user: User = Depends(get_current_user)
):
    try:
        if not request.question.strip():
            raise HTTPException(
                status_code=400,
                detail="Question cannot be empty"
            )

        result = handle_sql_question(request.question)

        return {
            "question": request.question,
            "result": result
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while retrieving analytics"
        )


# Authenticated Incident Report API
@app.get("/report")
def generate_report(
    current_user: User = Depends(get_current_user)
):
    try:
        report = generate_incident_report()

        return {
            "report_type": "Incident Summary Report",
            "report": str(report)
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while generating the report"
        )
