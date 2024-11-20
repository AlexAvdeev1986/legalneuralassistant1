from django.urls import path
from . import views

app_name = 'legal_app'

urlpatterns = [
    path('', views.home, name='home'),
    path('chat/', views.chat, name='chat'),
    path('document-generator/', views.document_generator, name='document_generator'),
]
