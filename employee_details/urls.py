from django.urls import path
from .views import device_logs

urlpatterns = [
    path('logs/', device_logs, name='device_logs'),
]   