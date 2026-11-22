
import requests
import os

API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "http://127.0.0.1:8000"
)


def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


# AUTHENTICATION

def register_user(username, email, password):
    return requests.post(
        f"{API_BASE_URL}/auth/register",
        json={"username": username, "email": email, "password": password},
        timeout=30
    )


def login_user(username, password):
    return requests.post(
        f"{API_BASE_URL}/auth/login",
        json={"username": username, "password": password},
        timeout=30
    )


def get_user_profile(token):
    return requests.get(
        f"{API_BASE_URL}/auth/me",
        headers=auth_headers(token),
        timeout=30
    )


def logout_user():
    return True


# CLINICAL CHAT

def chat_with_assistant(question, token):
    return requests.post(
        f"{API_BASE_URL}/chat",
        json={"question": question},
        headers=auth_headers(token),
        timeout=180
    )


# HOSPITAL ANALYTICS

def get_analytics(question, token):
    return requests.post(
        f"{API_BASE_URL}/analytics",
        json={"question": question},
        headers=auth_headers(token),
        timeout=60
    )


# INCIDENT REPORTS

def get_incident_report(token):
    return requests.get(
        f"{API_BASE_URL}/report",
        headers=auth_headers(token),
        timeout=60
    )


# USER MANAGEMENT

def get_all_users(token):
    return requests.get(
        f"{API_BASE_URL}/auth/users",
        headers=auth_headers(token),
        timeout=30
    )


def create_user(token, username, email, password, role):
    return requests.post(
        f"{API_BASE_URL}/auth/users",
        headers=auth_headers(token),
        json={
            "username": username,
            "email": email,
            "password": password,
            "role": role
        },
        timeout=30
    )


# ---------------- DOCUMENT MANAGEMENT ----------------

def upload_document(token, uploaded_file):
    return requests.post(
        f"{API_BASE_URL}/documents/upload",
        headers=auth_headers(token),
        files={
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                uploaded_file.type or "application/octet-stream"
            )
        },
        timeout=180
    )


def get_documents(token):
    return requests.get(
        f"{API_BASE_URL}/documents/",
        headers=auth_headers(token),
        timeout=30
    )


def delete_document(token, filename):
    return requests.delete(
        f"{API_BASE_URL}/documents/{filename}",
        headers=auth_headers(token),
        timeout=180
    )


def reindex_documents(token):
    return requests.post(
        f"{API_BASE_URL}/documents/reindex",
        headers=auth_headers(token),
        timeout=180
    )
