from apscheduler.schedulers.background import BackgroundScheduler
import logging
from app.models.user_model import User

def start_scheduler():
    """
    Start the background scheduler to remove expired tokens daily.
    """
    try:
        scheduler = BackgroundScheduler()
        scheduler.add_job(User.remove_expired_tokens, 'interval', days=1)
        scheduler.start()
        logging.info("Scheduler started successfully.")
    except Exception as e:
        logging.error(f"Error starting scheduler: {e}")
