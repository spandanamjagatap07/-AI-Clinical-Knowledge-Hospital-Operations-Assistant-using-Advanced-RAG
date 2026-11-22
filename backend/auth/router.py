
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database.models import User
from backend.auth.dependencies import get_db, get_current_user, require_roles
from backend.auth.security import (
    hash_password,
    verify_password,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from backend.auth.schemas import (
    UserRegister,
    UserLogin,
    AdminUserCreate,
    UserResponse,
    TokenResponse
)


router = APIRouter(prefix="/auth", tags=["Authentication"])


def create_user_record(user_data, db: Session, role: str):
    username = user_data.username.strip()
    email = str(user_data.email).lower().strip()

    if not username:
        raise HTTPException(
            status_code=400,
            detail="Username cannot be empty"
        )

    if db.query(User).filter(User.username == username).first():
        raise HTTPException(
            status_code=409,
            detail="Username already exists"
        )

    if db.query(User).filter(User.email == email).first():
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

    user = User(
        username=username,
        email=email,
        hashed_password=hash_password(user_data.password),
        role=role,
        is_active=True
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


# Public registration: new users always receive the nurse role.
@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register_user(
    request: UserRegister,
    db: Session = Depends(get_db)
):
    return create_user_record(request, db, "nurse")


# Login: verify credentials and issue a JWT.
@router.post("/login", response_model=TokenResponse)
def login(
    request: UserLogin,
    db: Session = Depends(get_db)
):
    username = request.username.strip()

    user = db.query(User).filter(User.username == username).first()

    if not user or not verify_password(
        request.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This account is inactive"
        )

    token = create_access_token(user.user_id, user.role)

    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in_minutes": ACCESS_TOKEN_EXPIRE_MINUTES,
        "user": user
    }


# Get details of the currently authenticated user.
@router.get("/me", response_model=UserResponse)
def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    return current_user


# Only an admin can create accounts with assigned roles.
@router.post(
    "/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def admin_create_user(
    request: AdminUserCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_roles("admin"))
):
    return create_user_record(request, db, request.role)


# Admin-only list of users.
@router.get("/users", response_model=list[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    admin: User = Depends(require_roles("admin"))
):
    return db.query(User).order_by(User.user_id).all()
