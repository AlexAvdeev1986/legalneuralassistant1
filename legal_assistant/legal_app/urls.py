from django.urls import path
from . import views

urlpatterns = [
    path('chat/', views.chat, name='chat'),
    path('document_generator/', views.document_generator, name='document_generator'),
]
