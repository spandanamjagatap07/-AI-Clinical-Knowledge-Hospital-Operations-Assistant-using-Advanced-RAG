
from pathlib import Path
from document_loader import load_directory

# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Hospital document and dataset folders
DOCUMENTS_PATH = PROJECT_ROOT / "data" / "documents"
DATASETS_PATH = PROJECT_ROOT / "data" / "datasets"

print("\n========== LOADING HOSPITAL DOCUMENTS ==========")

documents = load_directory(DOCUMENTS_PATH)

print("\n========== LOADING HOSPITAL DATASETS ==========")

datasets = load_directory(DATASETS_PATH)

all_documents = documents + datasets

print("\n========== FINAL RESULTS ==========")

print("Hospital documents:", len(documents))
print("Dataset document units:", len(datasets))
print("Total document units:", len(all_documents))

if all_documents:
    print("\n========== SAMPLE DOCUMENT ==========")
    print("Content:")
    print(all_documents[0].page_content[:500])

    print("\nMetadata:")
    print(all_documents[0].metadata)
else:
    print("No documents were loaded.")
