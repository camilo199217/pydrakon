import uuid
import jwt
from datetime import datetime, timedelta
from secureauthapi.conf import get_settings

settings = get_settings()


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRATION)
    to_encode.update(
        {"exp": expire, "jti": str(uuid.uuid4())}  # identificador único del token
    )
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt
