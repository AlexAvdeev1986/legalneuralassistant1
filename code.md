# Legal Neural Assistant

Legal Neural Assistant — это приложение на базе Django, разработанное для помощи пользователям в генерации юридических документов и ответах на правовые вопросы через удобный интерфейс чат-бота. Приложение использует OpenAI API для генерации документов и ответов, что делает его полезным инструментом для первичной юридической поддержки.

## Структура проекта

 
 # project structure
legal_assistant/
├── manage.py
├── requirements.txt
├── .env
├── legal_assistant/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── legal_app/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── urls.py
    ├── views.py
    ├── forms.py
    ├── utils.py
    ├── templates/
    │   └── legal_app/
    │       ├── base.html
    │       ├── home.html
    │       ├── chat.html
    │       └── document_generator.html
    └── static/
        └── legal_app/
            ├── css/
            │   └── style.css
            └── js/
                └── main.js
 
 
 legal_assistant/
├── manage.py
#!/usr/bin/env python
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'legal_assistant.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()

├── requirements.txt
Django==4.2.7
python-dotenv==1.0.0
openai==1.3.5
django-crispy-forms==2.1
crispy-bootstrap4==2022.1
python-docx==1.0.1
markdown==3.5.1


├── .env
├── legal_assistant/
│   ├── __init__.py
│   ├── settings.py
# legal_assistant/settings.py
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'crispy_bootstrap4',
    'legal_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'legal_assistant.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'legal_assistant.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

LOGIN_URL = '/accounts/login/' 

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",  # Путь к вашим статическим файлам
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

# OpenAI API settings
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

│   ├── urls.py
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

│   └── wsgi.py
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'legal_assistant.settings')

application = get_wsgi_application()

└── legal_app/
    ├── __init__.py
    ├── admin.py
    from django.contrib import admin
from .models import LegalQuestion, Document

@admin.register(LegalQuestion)
class LegalQuestionAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'answer', 'created_at', 'category')
    search_fields = ('user__username', 'question', 'category')
    list_filter = ('category', 'created_at')

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'document_type', 'created_at')
    search_fields = ('title', 'document_type')
    list_filter = ('document_type', 'created_at')

    ├── apps.py
    from django.apps import AppConfig


class LegalAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'legal_app'

    ├── models.py
    from django.db import models
from django.contrib.auth.models import User

class LegalQuestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=100)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.question[:50]}"

class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    document_type = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='documents/', null=True, blank=True)

    def __str__(self):
        return self.title

    ├── urls.py
    from django.urls import path
from . import views

urlpatterns = [
    path('chat/', views.chat, name='chat'),
    path('document_generator/', views.document_generator, name='document_generator'),
]

    ├── views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import LegalQuestionForm, DocumentGeneratorForm
from .models import LegalQuestion, Document
from .utils import LegalAI
import json

# Используем один экземпляр LegalAI
legal_ai = LegalAI()

def home(request):
    return render(request, 'legal_app/home.html')

@login_required
def chat(request):
    if request.method == 'POST':
        form = LegalQuestionForm(request.POST)
        if form.is_valid():
            question = form.cleaned_data['question']
            
            # Получаем ответ на вопрос
            try:
                response = legal_ai.get_legal_response(question)
                legal_question = LegalQuestion(
                    user=request.user,
                    question=question,
                    answer=response['answer'],
                    category=response['category']
                )
                legal_question.save()
                
                return JsonResponse({
                    'status': 'success',
                    'answer': response['answer'],
                    'category': response['category']
                })
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': str(e)})
        
        return JsonResponse({'status': 'error', 'errors': form.errors})
    
    form = LegalQuestionForm()
    questions = LegalQuestion.objects.filter(user=request.user)
    return render(request, 'legal_app/chat.html', {'form': form, 'questions': questions})

@login_required(login_url='/accounts/login/')
def document_generator(request):
    if request.method == 'POST':
        form = DocumentGeneratorForm(request.POST)
        if form.is_valid():
            try:
                doc_type = form.cleaned_data['document_type']
                context = form.cleaned_data['context']  # Предполагается, что это строка JSON
                
                # Генерация контента с помощью LegalAI
                document_content = legal_ai.generate_document(doc_type, context)
                
                # Сохранение документа в базе данных
                document = Document(
                    user=request.user,
                    title=f"{doc_type}_{request.user.username}",
                    content=document_content,
                    document_type=doc_type
                )
                document.save()
                
                return JsonResponse({
                    'status': 'success',
                    'content': document_content
                })
            except json.JSONDecodeError:
                return JsonResponse({'status': 'error', 'message': 'Invalid JSON format for context.'})
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': str(e)})
        
        return JsonResponse({'status': 'error', 'errors': form.errors})
    
    form = DocumentGeneratorForm()
    documents = Document.objects.filter(user=request.user)
    return render(request, 'legal_app/document_generator.html', {
        'form': form,
        'documents': documents
    })

    ├── forms.py
    # legal_app/forms.py
from django import forms
from .models import LegalQuestion, Document

class LegalQuestionForm(forms.ModelForm):
    class Meta:
        model = LegalQuestion
        fields = ['question']
        widgets = {
            'question': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'})
        }

class DocumentGeneratorForm(forms.Form):
    DOCUMENT_TYPES = [
        ('complaint', 'Жалоба'),
        ('contract', 'Договор'),
        ('statement', 'Заявление'),
        ('pretension', 'Претензия'),
    ]
    
    document_type = forms.ChoiceField(
        choices=DOCUMENT_TYPES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    context = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 6,
            'class': 'form-control',
            'placeholder': 'Введите необходимые данные для документа в формате JSON'
        })
    )

    ├── utils.py
    # legal_app/utils.py

import openai
from django.conf import settings
from typing import Dict, Any
import json

class LegalAI:
    def __init__(self):
        # Set the OpenAI API key from the Django settings
        openai.api_key = settings.OPENAI_API_KEY

    def get_legal_response(self, question: str) -> Dict[str, Any]:
        """
        Sends a legal question to the OpenAI API and returns the answer and category.

        Parameters:
            question (str): The legal question to be answered.

        Returns:
            Dict[str, Any]: A dictionary containing the answer and the category.
        """
        try:
            # Send the user's question to OpenAI for a response
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Вы - юридический ассистент. Предоставьте точную и актуальную информацию по законодательству РФ."},
                    {"role": "user", "content": question}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            # Extract the answer from the OpenAI response
            answer = response.choices[0].message.content
            
            # Send the question again to determine the category
            category_response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Определите категорию юридического вопроса (например: гражданское право, уголовное право, административное право и т.д.)"},
                    {"role": "user", "content": question}
                ],
                temperature=0.3,
                max_tokens=50
            )
            
            # Extract the category from the OpenAI response
            category = category_response.choices[0].message.content.strip()
            
            return {
                'answer': answer,
                'category': category
            }
            
        except Exception as e:
            # Return an error message if an exception occurs
            return {
                'answer': f"Произошла ошибка при обработке запроса: {str(e)}",
                'category': 'Ошибка'
            }

    def generate_document(self, doc_type: str, context: dict) -> str:
        """
        Generates a document based on a specified type and context using the OpenAI API.

        Parameters:
            doc_type (str): The type of document to generate (e.g., "complaint", "contract").
            context (dict): The context data required to generate the document.

        Returns:
            str: The generated document content.
        """
        try:
            # Create a prompt with the document type and context data
            prompt = f"Сгенерируйте {doc_type} на основе следующих данных:\n"
            prompt += json.dumps(context, ensure_ascii=False, indent=2)
            
            # Request document content from OpenAI
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Вы - юридический ассистент. Создайте юридический документ по предоставленному шаблону и данным."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=2000
            )
            
            # Return the document content from the OpenAI response
            return response.choices[0].message.content
            
        except Exception as e:
            # Return an error message if an exception occurs
            return f"Ошибка при генерации документа: {str(e)}"

    ├── templates/
    │   └── legal_app/
    │       ├── base.html
    # legal_app/templates/legal_app/base.html
{% load static %}
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Юридический ассистент{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="{% static 'legal_app/css/style.css' %}" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="{% url 'home' %}">Юридический ассистент</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'chat' %}">Консультация</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'document_generator' %}">Генератор документов</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="container mt-4">
        {% block content %}
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script src="{% static 'legal_app/js/main.js' %}"></script>
</body>
</html>
{% endblock %}
    │       ├── home.html
    {% extends 'legal_app/base.html' %}
{% block content %}
<div class="jumbotron">
    <h1 class="display-4">Добро пожаловать в Юридический ассистент</h1>
    <p class="lead">Получите профессиональную юридическую консультацию и помощь в составлении документов</p>
    <hr class="my-4">
    <p>Выберите нужный вам сервис:</p>
    <a class="btn btn-primary btn-lg" href="{% url 'chat' %}" role="button">Получить консультацию</a>
    <a class="btn btn-secondary btn-lg" href="{% url 'document_generator' %}" role="button">Создать документ</a>
</div>
{% endblock %}

    │       └── document_generator.html
{% extends 'legal_app/base.html' %}
{% load crispy_forms_tags %}

{% block content %}
<div class="row">
    <div class="col-md-8">
        <div class="card">
            <div class="card-header">
                <h5 class="card-title mb-0">Генератор документов</h5>
            </div>
            <div class="card-body">
                <form id="documentForm" method="post">
                    {% csrf_token %}
                    {{ form|crispy }}
                    <button type="submit" class="btn btn-primary">Создать документ</button>
                </form>
                <div id="documentContent" class="mt-4"></div>
            </div>
        </div>
    </div>
    <div class="col-md-4">
        <div class="card">
            <div class="card-header">
                <h5 class="card-title mb-0">История документов</h5>
            </div>
            <div class="card-body">
                <div class="list-group">
                    {% for document in documents %}
                        <a href="#" class="list-group-item list-group-item-action">
                            {{ document.title }} - {{ document.document_type }} - {{ document.created_at }}
                        </a>
                    {% endfor %}
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

    └── static/
        └── legal_app/
            ├── css/
            body {
    background-color: #f8f9fa;
}

.card {
    margin-bottom: 20px;
}

.btn-primary {
    background-color: #0056b3;
    border-color: #0056b3;
}

.navbar-dark .navbar-nav .nav-link {
    color: rgba(255, 255, 255, 0.9);
}

            │   └── style.css
            └── js/
                └── main.js
                document.addEventListener('DOMContentLoaded', function () {
    const questionForm = document.getElementById('questionForm');
    const responseDiv = document.getElementById('response');

    if (questionForm) {
        questionForm.addEventListener('submit', function (e) {
            e.preventDefault();
            fetch(questionForm.action, {
                method: 'POST',
                body: new FormData(questionForm),
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    responseDiv.innerHTML = `<div class="alert alert-success">${data.answer}</div>`;
                } else {
                    responseDiv.innerHTML = `<div class="alert alert-danger">Произошла ошибка.</div>`;
                }
            });
        });
    }

    const documentForm = document.getElementById('documentForm');
    const documentContentDiv = document.getElementById('documentContent');

    if (documentForm) {
        documentForm.addEventListener('submit', function (e) {
            e.preventDefault();
            fetch(documentForm.action, {
                method: 'POST',
                body: new FormData(documentForm),
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    documentContentDiv.innerHTML = `<div class="alert alert-success">${data.content}</div>`;
                } else {
                    documentContentDiv.innerHTML = `<div class="alert alert-danger">Произошла ошибка.</div>`;
                }
            });
        });
    }
});
