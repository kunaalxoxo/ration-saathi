# FILE: ration-saathi/backend/app/worker.py
from celery import Celery
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Initialize Celery
celery_app = Celery(
    "ration_saathi",
    broker=f"redis://{settings.UPSTASH_REDIS_REST_URL}",
    backend=f"redis://{settings.UPSTASH_REDIS_REST_URL}",
    include=[
        'app.worker.tasks'
    ]
)

# Configure Celery
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
    worker_prefetch_multiplier=1,
    task_acks_late=True,
)

# Task routing
celery_app.conf.task_routes = {
    'app.worker.tasks.send_callback_call': {'queue': 'callbacks'},
    'app.worker.tasks.update_fps_risk_score': {'queue': 'analytics'},
    'app.worker.tasks.sync_case_to_government_portal': {'queue': 'government_sync'},
}

if __name__ == '__main__':
    celery_app.start()
