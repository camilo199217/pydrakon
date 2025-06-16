from secureauthapi.models.audit_event import AuditEvent
from sqlmodel import Session
from fastapi import Request


async def audit_event(
    request: Request, session: Session, action: str, success: bool, username: str = None
):
    ip = request.client.host
    user_agent = request.headers.get("user-agent")
    endpoint = request.url.path
    method = request.method

    event = AuditEvent(
        username=username,
        ip_address=ip,
        user_agent=user_agent,
        endpoint=endpoint,
        method=method,
        action=action,
        success=success,
    )
    session.add(event)
    session.commit()
