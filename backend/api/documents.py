
import shutil
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from backend.auth.dependencies import require_roles
from backend.database.models import User

from backend.rag.document_loader import load_directory
from backend.rag.text_chunking import split_documents
from backend.rag.vector_store import create_vector_store, VECTOR_DB_PATH


router = APIRouter(
    prefix="/documents",
    tags=["Document Management"]
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DOCUMENTS_DIR = PROJECT_ROOT / "data" / "documents"

ALLOWED_EXTENSIONS = {
    ".txt", ".pdf", ".docx", ".csv", ".xlsx", ".xls"
}

MAX_FILE_SIZE = 20 * 1024 * 1024


def rebuild_knowledge_base():
    """Rebuild the Chroma database from all available documents."""

    documents = load_directory(str(DOCUMENTS_DIR))

    if not documents:
        shutil.rmtree(VECTOR_DB_PATH, ignore_errors=True)
        return 0

    chunks = split_documents(documents)

    shutil.rmtree(VECTOR_DB_PATH, ignore_errors=True)

    create_vector_store(chunks)

    return len(chunks)


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(require_roles("admin"))
):
    DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)

    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is missing.")

    filename = Path(file.filename).name
    extension = Path(filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file format."
        )

    destination = DOCUMENTS_DIR / filename

    if destination.exists():
        raise HTTPException(
            status_code=409,
            detail="A document with this filename already exists."
        )

    content = await file.read()

    if not content:
        raise HTTPException(status_code=400, detail="File is empty.")

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File exceeds the 20 MB upload limit."
        )

    try:
        destination.write_bytes(content)

        chunk_count = rebuild_knowledge_base()

        return {
            "message": "Document uploaded and indexed successfully.",
            "filename": filename,
            "chunks_created": chunk_count
        }

    except Exception as error:
        destination.unlink(missing_ok=True)

        raise HTTPException(
            status_code=500,
            detail=f"Document upload or indexing failed: {str(error)}"
        )


@router.get("/")
def list_documents(
    current_user: User = Depends(require_roles("admin"))
):
    DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)

    documents = []

    for path in sorted(DOCUMENTS_DIR.iterdir()):
        if path.is_file() and path.suffix.lower() in ALLOWED_EXTENSIONS:
            documents.append({
                "filename": path.name,
                "extension": path.suffix.lower(),
                "size_kb": round(path.stat().st_size / 1024, 2)
            })

    return {
        "total_documents": len(documents),
        "documents": documents
    }


@router.delete("/{filename}")
def delete_document(
    filename: str,
    current_user: User = Depends(require_roles("admin"))
):
    safe_filename = Path(filename).name

    if safe_filename != filename:
        raise HTTPException(status_code=400, detail="Invalid filename.")

    destination = DOCUMENTS_DIR / safe_filename

    if not destination.is_file():
        raise HTTPException(status_code=404, detail="Document not found.")

    destination.unlink()

    try:
        chunk_count = rebuild_knowledge_base()

        return {
            "message": "Document deleted and knowledge base updated.",
            "filename": safe_filename,
            "chunks_created": chunk_count
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Document deleted, but re-indexing failed: {str(error)}"
        )


@router.post("/reindex")
def reindex_documents(
    current_user: User = Depends(require_roles("admin"))
):
    try:
        chunk_count = rebuild_knowledge_base()

        return {
            "message": "Knowledge base re-indexed successfully.",
            "chunks_created": chunk_count
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Re-indexing failed: {str(error)}"
        )
