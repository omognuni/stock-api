from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    
    def ready(self):   
        print("start Scheduler....")
        from core.scheduler import scheduler
        scheduler.start()