from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_resources, name='view_resources'),
    path('upload_resources/', views.upload_resources, name='upload_resources'),
    path('delete_and_upload_resources/',views.delete_and_upload_resources, name='delete_and_upload_resources'),
]
