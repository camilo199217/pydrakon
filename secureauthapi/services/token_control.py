import jwt
from sqlmodel import Session, select
from secureauthapi.models.revoked_token import RevokedToken
from secureauthapi.conf import get_settings

settings = get_settings()


def revoke_token(token: str, session: Session):
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        jti = payload.get("jti")
        if jti:
            revoked = RevokedToken(jti=jti)
            session.add(revoked)
            session.commit()
    except jwt.JWTError:
        pass


def is_token_revoked(token: str, session: Session) -> bool:
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        jti = payload.get("jti")
        if jti:
            stmt = select(RevokedToken).where(RevokedToken.jti == jti)
            return session.exec(stmt).first() is not None
        return True  # si no hay jti, lo tratamos como inválido
    except jwt.JWTError:
        return True
