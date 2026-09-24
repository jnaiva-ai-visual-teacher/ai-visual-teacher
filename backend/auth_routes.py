from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session

from database import get_db
from models import User, UserSession
from schemas import SignupRequest, LoginRequest, UserResponse
from auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
    generate_session_token,
    hash_session_token,
    SESSION_EXPIRE_DAYS
)


router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


@router.post("/signup", response_model=UserResponse)
def signup(
    user_data: SignupRequest,
    db: Session = Depends(get_db)
):

    email = user_data.email.lower()

    existing_user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered"
        )

    new_user = User(
        name=user_data.name,
        email=email,
        password_hash=hash_password(user_data.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login", response_model=UserResponse)
def login(
    user_data: LoginRequest,
    response: Response,
    db: Session = Depends(get_db)
):
    email = user_data.email.lower()

    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Create short-lived access token
    access_token = create_access_token(user.id)

    # Create long-lived session token
    session_token = generate_session_token()
    session_token_hash = hash_session_token(session_token)

    session = UserSession(
        user_id=user.id,
        token_hash=session_token_hash,
        expires_at=datetime.now(timezone.utc) + timedelta(days=SESSION_EXPIRE_DAYS)
    )

    db.add(session)
    db.commit()

    # Access token: 15 minutes
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=60 * 15,
        path="/"
    )

    # Session token: 30 days
    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=60 * 60 * 24 * SESSION_EXPIRE_DAYS,
        path="/"
    )

    return user

@router.post("/refresh", response_model=UserResponse)
def refresh_session(
    response: Response,
    db: Session = Depends(get_db)
):
    session_token = None

    # We need the request to read the session cookie.

@router.post("/refresh", response_model=UserResponse)
def refresh_session(
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):
    session_token = request.cookies.get("session_token")

    if not session_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No active session"
        )

    token_hash = hash_session_token(session_token)

    session = (
        db.query(UserSession)
        .filter(UserSession.token_hash == token_hash)
        .first()
    )

    if not session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid session"
        )

    now = datetime.now(timezone.utc)

    if session.expires_at <= now:
        db.delete(session)
        db.commit()

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired"
        )

    user = db.get(User, session.user_id)

    if not user:
        db.delete(session)
        db.commit()

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    # Create a new short-lived access token
    access_token = create_access_token(user.id)

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=60 * 15,
        path="/"
    )

    # Extend the session for another 30 days
    session.expires_at = now + timedelta(days=SESSION_EXPIRE_DAYS)
    db.commit()

    return user

@router.post("/logout")
def logout(
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):
    session_token = request.cookies.get("session_token")

    if session_token:
        token_hash = hash_session_token(session_token)

        session = (
            db.query(UserSession)
            .filter(UserSession.token_hash == token_hash)
            .first()
        )

        if session:
            db.delete(session)
            db.commit()

    response.delete_cookie(
        key="access_token",
        path="/"
    )

    response.delete_cookie(
        key="session_token",
        path="/"
    )

    return {"message": "Logged out successfully"}

@router.get("/me", response_model=UserResponse)
def get_me(
    current_user: User = Depends(get_current_user)
):

    return current_user