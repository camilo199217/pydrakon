from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class RevokedToken(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    jti: str = Field(index=True, unique=True)
    revoked_at: datetime = Field(default_factory=datetime.utcnow)
