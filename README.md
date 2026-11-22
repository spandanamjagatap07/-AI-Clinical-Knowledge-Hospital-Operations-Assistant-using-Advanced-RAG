# 🏥 AI-Powered Hospital Assistant

An intelligent hospital management and clinical knowledge assistance system powered by Artificial Intelligence, Retrieval-Augmented Generation (RAG), and Large Language Models (LLMs).

The system helps hospital administrators and healthcare staff access clinical knowledge, analyze hospital data, generate incident reports, and interact with hospital information through an AI-powered conversational interface.

---

## 📌 Project Overview

The AI-Powered Hospital Assistant is designed to simplify hospital information management by integrating Artificial Intelligence with hospital databases and clinical documents.

It combines three major capabilities:

1. **Clinical Knowledge Assistant:** Uses Retrieval-Augmented Generation (RAG) to retrieve relevant information from uploaded hospital documents and generate context-aware answers.
2. **Hospital Data Analytics:** Retrieves and analyzes structured hospital data using SQL queries.
3. **Automated Report Generation:** Generates structured hospital incident reports based on available hospital records.

The application provides a user-friendly interface through which authorized users can interact with these capabilities.

---

## ✨ Key Features

### 1. User Authentication
- User registration and login.
- JWT-based authentication.
- Secure access to protected application features.
- User information retrieval.

### 2. AI Clinical Knowledge Assistant
- Upload hospital-related documents.
- Extract and process document content.
- Document chunking and embedding generation.
- Semantic search using ChromaDB.
- Retrieval-Augmented Generation (RAG).
- Context-aware responses using Groq LLM.

### 3. Hospital Data Analytics
- Retrieve structured hospital information.
- Perform SQL-based data analysis.
- Answer questions about hospital records.
- Generate insights from hospital database information.

### 4. Automated Incident Report Generation
- Generate hospital incident reports.
- Summarize incident information.
- Categorize incidents according to severity.
- Present structured incident summaries.

### 5. Document Management
- Upload clinical documents.
- View available documents.
- Delete uploaded documents.
- Reindex documents for retrieval.

### 6. Interactive Dashboard
- Streamlit-based frontend.
- User-friendly navigation.
- Interactive AI chat interface.
- Access to analytics and report generation.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Frontend development |
| FastAPI | Backend REST API |
| Groq LLM | AI-powered response generation |
| ChromaDB | Vector database |
| Embedding Models | Text embedding generation |
| SQLAlchemy | Database interaction |
| JWT | Authentication |
| REST API | Frontend-backend communication |
| Docker | Containerization and deployment |

---

## 🏗️ System Architecture

The application follows a modular client-server architecture.

**Frontend Layer**
- Developed using Streamlit.
- Provides authentication, chat, analytics, and reporting interfaces.

**Backend Layer**
- Developed using FastAPI.
- Handles authentication, API requests, document processing, and AI workflows.

**AI Processing Layer**
- Routes user queries to the appropriate processing module.
- Uses RAG for clinical document queries.
- Uses SQL analytics for structured hospital data.
- Uses report generation for incident summaries.

**Data Layer**
- ChromaDB stores document embeddings.
- Hospital database stores structured records.
- Uploaded documents are maintained for retrieval and processing.

---

## 📂 Project Structure

```text
AI Hospital/
│
├── backend/
│   ├── api/
│   ├── models.py
│   ├── database.py
│   └── ...
│
├── frontend/
│   ├── app.py
│   └── ...
│
├── data/
│
├── evaluation/
│
├── chroma_db/
│
├── chroma_parent_child/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env
├── test_streamlit.py
└── README.md
```

## 🔗 Backend API Endpoints

The FastAPI backend exposes the following REST API endpoints:

| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Authenticate a user |
| GET | `/auth/me` | Retrieve current user details |
| POST | `/chat` | Process AI chat queries |
| POST | `/analytics` | Perform hospital data analytics |
| POST | `/report` | Generate incident reports |
| GET | `/auth/users` | Retrieve user information |
| POST | `/documents/upload` | Upload documents |
| GET | `/documents/` | View uploaded documents |
| DELETE | `/documents/{filename}` | Delete a document |
| POST | `/documents/reindex` | Reindex documents |

---

## 🔄 Application Workflow

1. The user logs into the application.
2. The user submits a question or selects a functionality.
3. The frontend sends the request to the FastAPI backend.
4. The backend processes and routes the request.
5. Depending on the request:
   - Clinical queries are handled through the RAG pipeline.
   - Hospital data queries are processed through SQL analytics.
   - Incident report requests are handled by the report generation module.
6. The AI processing layer generates the required response.
7. The backend returns the result to the frontend.
8. The frontend displays the response to the user.

---

## 🎯 Project Objectives

- To integrate Artificial Intelligence into hospital information management.
- To provide intelligent access to clinical knowledge.
- To reduce manual effort in retrieving hospital information.
- To automate hospital incident report generation.
- To support data-driven hospital decision-making.
- To provide a centralized and user-friendly AI assistance platform.

---

## 🔮 Future Enhancements

- Integration with hospital management systems.
- Advanced hospital data visualization.
- Voice-based AI interaction.
- Enhanced role-based access control.
- Multilingual support.
- Improved clinical document retrieval.
- Advanced reporting and predictive analytics.

---

## ⚠️ Disclaimer

This project is developed for educational and demonstration purposes.

AI-generated responses should not be considered a substitute for professional medical advice, diagnosis, or treatment. Clinical information must be verified by qualified healthcare professionals before being used in patient care.

---

## 👩‍💻 Author

**AI-Powered Hospital Assistant Project**

Developed using Python, FastAPI, Streamlit, RAG, ChromaDB, and Groq LLM.

---
