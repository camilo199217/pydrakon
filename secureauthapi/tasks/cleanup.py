from datetime import datetime, timedelta
from secureauthapi.models.audit_event import AuditEvent
from secureauthapi.services.db import get_session
from sqlmodel import Session, select
import logging


def clean_old_audit_logs(retention_days: int = 180):
    with Session(get_session()) as session:
        cutoff = datetime.utcnow() - timedelta(days=retention_days)
        stmt = select(AuditEvent).where(AuditEvent.timestamp < cutoff)
        results = session.exec(stmt).all()

        count = len(results)
        for record in results:
            session.delete(record)
        session.commit()

        logging.info(f"🧹 Limpieza de auditoría: {count} registros eliminados")
