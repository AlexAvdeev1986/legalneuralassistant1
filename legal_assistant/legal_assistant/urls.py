"""
URL configuration for legal_assistant project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from legal_app import views

urlpatterns = [
    path('admin/', admin.site.urls),  # Админка Django
    path('accounts/', include('django.contrib.auth.urls')),  # Стандартные URL для аутентификации
    path('', views.home, name='home'),  # Главная страница
    path('chat/', views.chat, name='chat'),  # Страница чата
    path('document_generator/', views.document_generator, name='document_generator'),  # Страница генерации документов
    path('legal_app/', include('legal_app.urls')),  # Подключаем дополнительные URL для legal_app
]
