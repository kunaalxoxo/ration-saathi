from celery import Celery
from app.core.config import settings
from app.services.sms import sms_service
from twilio.rest import Client as TwilioClient
import asyncio


celery_app = Celery(
    "ration_saathi",
    broker=f"redis://{settings.UPSTASH_REDIS_REST_URL.split('//')[1]}",
    backend=f"redis://{settings.UPSTASH_REDIS_REST_URL.split('//')[1]}"
)


celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Asia/Kolkata',
    enable_utc=True
)


@celery_app.task(name="tasks.send_sms")
def send_sms_task(phone: str, cn: str, lang: str):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        sms_service.send_case_created_sms(phone, cn, lang)
    )


@celery_app.task(name="tasks.update_fps_risk_score")
def update_fps_risk_score_task(fps: str):
    from app.services.analytics import analytics_service
    analytics_service.calculate_fps_risk_score(fps)


@celery_app.task(name="tasks.send_callback_call")
def send_callback_call_task(to: str):
    client = TwilioClient(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    base_url = settings.EPDS_API_BASE_URL or ""
    url = f"{base_url.replace('/api', '')}/ivr/inbound"
    client.calls.create(to=to, from_=settings.TWILIO_PHONE_NUMBER, url=url)
