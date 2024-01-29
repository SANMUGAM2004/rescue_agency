# chat/urls.py
from django.urls import path
from .views import open_chat, send_message
from . import views

urlpatterns = [
    path('', views.open_chat, name='open_chat'),
    path('send-message/', views.send_message, name='send_message'),
]
