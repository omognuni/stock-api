from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

from django.conf import settings
from django_apscheduler.jobstores import register_events

from scripts.load_csv import load_csv

def start():
    scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
    register_events(scheduler)
    
    # 매일 00시 00분 마다 csv 업데이트
    scheduler.add_job(
        load_csv,
        trigger=CronTrigger(hour='00',minute='00'),
        max_instances=1,
        name='load_csv',
    )
    
    scheduler.start()