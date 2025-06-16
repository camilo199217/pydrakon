from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import timedelta
from secureauthapi.tasks.cleanup import clean_old_audit_logs
import logging

scheduler = BackgroundScheduler()


def start_scheduler():
    scheduler.add_job(
        func=clean_old_audit_logs,
        trigger=IntervalTrigger(days=7),  # cada 7 días
        name="Purgar logs antiguos de auditoría",
        replace_existing=True,
    )
    scheduler.start()
    logging.info("🕒 Scheduler iniciado.")
