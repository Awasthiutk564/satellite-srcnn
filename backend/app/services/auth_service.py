from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password, create_access_token
from app.db.models.user import User
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from app.schemas.user import UserRead


def register_user(db: Session, data: RegisterRequest) -> UserRead:
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise ValueError("User with this email already exists")

    user = User(
        email=data.email,
        full_name=data.full_name,
        password_hash=get_password_hash(data.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserRead.model_validate(user)


def login_user(db: Session, data: LoginRequest) -> TokenResponse:
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise ValueError("Incorrect email or password")

    token = create_access_token(str(user.id))
    return TokenResponse(access_token=token)

