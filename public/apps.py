from django.apps import AppConfig
from .updater import start

class PublicConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'public'
    # start()