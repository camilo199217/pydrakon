import jwt
from fastapi.security import OAuth2PasswordBearer
from secureauthapi.conf import get_settings
from secureauthapi.models.user import User
from secureauthapi.core.security import get_password_hash, verify_password
from sqlmodel import Session, select
from fastapi import Depends, HTTPException

from secureauthapi.services.db import get_session
from secureauthapi.services.token_control import is_token_revoked

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
settings = get_settings()


def create_user(username: str, password: str, session: Session):
    user = session.exec(select(User).where(User.username == username)).first()
    if user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(password)
    new_user = User(username=username, hashed_password=hashed_password)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


def authenticate_user(username: str, password: str, session: Session):
    user = session.exec(select(User).where(User.username == username)).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def get_current_user(
    token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)
):
    if is_token_revoked(token, session):
        raise HTTPException(status_code=401, detail="Token has been revoked")

    payload = jwt.decode(
        token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
    )
    username = payload.get("sub")
