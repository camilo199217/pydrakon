from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class LoginAttempt(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    ip_address: str
    success: bool
    timestamp: datetime = Field(default_factory=datetime.utcnow)
