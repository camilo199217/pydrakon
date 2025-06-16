from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class AuditEvent(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: Optional[str] = Field(index=True)
    ip_address: str
    user_agent: Optional[str]
    endpoint: str
    method: str
    action: str  # ej: login, login_fail, access_protected
    success: bool
    timestamp: datetime = Field(default_factory=datetime.utcnow)
