import hashlib
import secrets
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from . import schemas, models
from .database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

bearer_scheme = HTTPBearer(auto_error=False)


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(password: str, password_hash: str) -> bool:
    return hash_password(password) == password_hash


def create_token() -> str:
    return secrets.token_hex(32)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> models.User:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    token = credentials.credentials
    user = db.query(models.User).filter(models.User.token == token).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    return user


def require_write_access(current_user: models.User = Depends(get_current_user)):
    if current_user.is_read_only:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User has read-only permissions",
        )
    return current_user


@router.post("/register", response_model=schemas.UserResponse)
def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(
        models.User.username == user_in.username
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken",
        )

    user = models.User(
        username=user_in.username,
        password_hash=hash_password(user_in.password),
        is_read_only=user_in.is_read_only,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=schemas.TokenResponse)
def login(user_in: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.username == user_in.username
    ).first()
    if not user or not verify_password(user_in.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    token = create_token()
    user.token = token
    db.add(user)
    db.commit()
    return schemas.TokenResponse(token=token)


@router.post("/logout")
def logout(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    current_user.token = None
    db.add(current_user)
    db.commit()
    return {"detail": "Logged out"}
