from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from secureauthapi.core import limiter
from secureauthapi.services.auth_service import (
    authenticate_user,
    create_user,
    oauth2_scheme,
)
from secureauthapi.core.jwt import create_access_token
from secureauthapi.services.audit import audit_event
from secureauthapi.services.db import get_session
from secureauthapi.services.login_tracker import is_blocked, register_login_attempt
from secureauthapi.services.token_control import revoke_token

router = APIRouter(prefix="/auth")


@router.post("/register")
def register(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = create_user(form_data.username, form_data.password, session)
    return {"message": "User registered successfully"}


@router.post("/login")
@limiter.limit("10/minute")
async def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    username = form_data.username
    ip = request.client.host

    if is_blocked(username, ip, session):
        await audit_event(
            request,
            session,
            action="login_blocked",
            success=False,
            username=username,
        )
        raise HTTPException(
            status_code=403,
            detail="Too many failed login attempts. Please wait a few minutes.",
        )

    user = authenticate_user(form_data.username, form_data.password, session)

    if not user:
        await audit_event(
            request, session, action="login_failed", success=False, username=username
        )

        register_login_attempt(username, ip, False, session)

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    register_login_attempt(username, ip, True, session)

    await audit_event(
        request, session, action="login_success", success=True, username=user.username
    )

    access_token = create_access_token({"sub": user.username})

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout")
async def logout(
    request: Request,
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
):
    revoke_token(token, session)
    await audit_event(request, session, action="logout", success=True)
    return {"message": "Token revoked"}
