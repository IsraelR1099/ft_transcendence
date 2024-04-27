from django.contrib import admin
from django.apps import AppConfig

# Register your models

class   UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'
