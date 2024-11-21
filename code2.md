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

# settings.py additions
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

# Rate limiting settings
RATELIMIT_ENABLE = True
RATELIMIT_USE_CACHE = 'default'
RATELIMIT_CACHE_PREFIX = 'rl:'

# Cache settings
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

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

app_name = 'legal_app'

urlpatterns = [
    path('', views.home, name='home'),
    path('chat/', views.chat, name='chat'),
    path('document-generator/', views.document_generator, name='document_generator'),
]


    ├── views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core.validators import validate_ipv46_address
from django_ratelimit.decorators import ratelimit
from .forms import LegalQuestionForm, DocumentGeneratorForm
from .models import LegalQuestion, Document
from .utils import LegalAI
import json
import logging
from functools import wraps
from typing import Any, Dict

# Initialize LegalAI instance and logger
legal_ai = LegalAI()
logger = logging.getLogger(__name__)

def format_russian_response(data: Dict[str, Any], status: int = 200) -> JsonResponse:
    """
    Форматирует ответ с поддержкой русского языка
    """
    return JsonResponse(data, json_dumps_params={'ensure_ascii': False}, status=status)

@ensure_csrf_cookie
def home(request):
    """
    Отображение главной страницы
    """
    return render(request, 'legal_app/home.html', {
        'title': 'Главная страница',
        'description': 'Юридический помощник с искусственным интеллектом'
    })

def handle_errors(view_func):
    """
    Decorator for handling common errors in views with Russian messages
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        try:
            return view_func(request, *args, **kwargs)
        except ValidationError as e:
            logger.warning(f"Validation error in {view_func.__name__}: {str(e)}")
            return format_russian_response({
                'status': 'error',
                'message': 'Ошибка валидации данных.'
            }, status=400)
        except json.JSONDecodeError as e:
            logger.warning(f"JSON decode error in {view_func.__name__}: {str(e)}")
            return format_russian_response({
                'status': 'error',
                'message': 'Некорректный формат JSON.'
            }, status=400)
        except Exception as e:
            logger.error(f"Error in {view_func.__name__}: {str(e)}", exc_info=True)
            return format_russian_response({
                'status': 'error',
                'message': 'Произошла внутренняя ошибка сервера.'
            }, status=500)
    return wrapper

def get_client_ip(request) -> str:
    """
    Get client IP address from request with validation
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    
    try:
        validate_ipv46_address(ip)
        return ip
    except ValidationError:
        return 'неизвестно'

@login_required
@require_http_methods(["GET", "POST"])
@ratelimit(key='user', rate='10/m', group='legal_chat')
@handle_errors
def chat(request):
    """
    Handle legal chat interactions with Russian responses
    """
    if request.method == 'POST':
        if getattr(request, 'limited', False):
            return format_russian_response({
                'status': 'error',
                'message': 'Превышен лимит запросов. Пожалуйста, подождите минуту.'
            }, status=429)
        
        form = LegalQuestionForm(request.POST)
        if form.is_valid():
            question = form.cleaned_data['question']
            user_ip = get_client_ip(request)
            
            try:
                response = legal_ai.get_legal_response(
                    question=question,
                    user_ip=user_ip
                )
                
                legal_question = LegalQuestion.objects.create(
                    user=request.user,
                    question=question,
                    answer=response['answer'],
                    category=response['category'],
                    ip_address=user_ip,
                    status='answered',
                    processing_time=response.get('processing_time')
                )
                
                return format_russian_response({
                    'status': 'success',
                    'answer': response['answer'],
                    'category': response['category'],
                    'question_id': legal_question.id
                })
            except Exception as e:
                logger.error(f"Error getting AI response: {str(e)}", exc_info=True)
                return format_russian_response({
                    'status': 'error',
                    'message': 'Не удалось получить ответ от сервиса. Пожалуйста, попробуйте позже.'
                }, status=500)
        
        return format_russian_response({
            'status': 'error',
            'errors': {k: [str(e) for e in v] for k, v in form.errors.items()}
        }, status=400)

    # GET request: display form and question history
    questions = LegalQuestion.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'legal_app/chat.html', {
        'form': LegalQuestionForm(),
        'questions': questions
    })

@login_required
@require_http_methods(["GET", "POST"])
@handle_errors
def document_generator(request):
    """
    Handle document generation requests with Russian responses
    """
    if request.method == 'POST':
        form = DocumentGeneratorForm(request.POST)
        if form.is_valid():
            try:
                doc_type = form.cleaned_data['document_type']
                title = form.cleaned_data['title']
                context_str = form.cleaned_data['context']
                
                # Parse and validate JSON context
                try:
                    context = json.loads(context_str)
                except json.JSONDecodeError:
                    return format_russian_response({
                        'status': 'error',
                        'message': 'Некорректный формат контекста. Убедитесь, что это валидный JSON.'
                    }, status=400)
                
                document_content = legal_ai.generate_document(doc_type, context)
                
                document = Document.objects.create(
                    user=request.user,
                    title=title,
                    content=document_content,
                    document_type=doc_type
                )
                
                return format_russian_response({
                    'status': 'success',
                    'content': document_content,
                    'document_id': document.id,
                    'message': 'Документ успешно создан'
                })
            except Exception as e:
                logger.error(f"Error generating document: {str(e)}", exc_info=True)
                return format_russian_response({
                    'status': 'error',
                    'message': 'Ошибка при генерации документа. Пожалуйста, попробуйте позже.'
                }, status=500)
        
        return format_russian_response({
            'status': 'error',
            'errors': {k: [str(e) for e in v] for k, v in form.errors.items()}
        }, status=400)

    # GET request: display form and document history
    documents = Document.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'legal_app/document_generator.html', {
        'form': DocumentGeneratorForm(),
        'documents': documents
    })


    ├── forms.py
    # legal_app/forms.py
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
    title = forms.CharField(max_length=200, required=True)

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

# legal_app/utils.py
import json
import logging
import time
from typing import Dict, Any
from django.conf import settings
from django.core.cache import cache
from openai import OpenAI

logger = logging.getLogger(__name__)

class LegalAI:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.cache_timeout = 3600

    def _get_cached_response(self, cache_key: str) -> Any:
        return cache.get(cache_key)

    def _cache_response(self, cache_key: str, response: Any):
        cache.set(cache_key, response, self.cache_timeout)

    def get_legal_response(self, question: str, user_ip: str = None) -> Dict[str, Any]:
        start_time = time.time()
        cache_key = f"legal_response_{hash(question)}"

        cached_response = self._get_cached_response(cache_key)
        if cached_response:
            logger.info("Response found in cache.")
            return cached_response

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Вы - юридический ассистент. Предоставьте точную и актуальную информацию по законодательству РФ."},
                    {"role": "user", "content": question}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            answer = response.choices[0].message.content

            category_response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Определите категорию юридического вопроса (гражданское право, уголовное право, административное право и т.д.)"},
                    {"role": "user", "content": question}
                ],
                temperature=0.3,
                max_tokens=50
            )
            category = category_response.choices[0].message.content.strip()

            result = {
                'answer': answer,
                'category': category,
                'processing_time': time.time() - start_time
            }

            self._cache_response(cache_key, result)
            logger.info("Response successfully generated and cached.")
            return result

        except Exception as e:
            logger.error(f"Error processing request: {e}", exc_info=True)
            return {
                'answer': f"Произошла ошибка при обработке запроса: {str(e)}",
                'category': 'Ошибка',
                'processing_time': time.time() - start_time
            }

    def generate_document(self, doc_type: str, context: Dict[str, Any]) -> str:
        cache_key = f"document_{hash(doc_type)}_{hash(json.dumps(context, sort_keys=True))}"

        cached_document = self._get_cached_response(cache_key)
        if cached_document:
            logger.info("Document found in cache.")
            return cached_document

        try:
            prompt = f"Сгенерируйте {doc_type} на основе следующих данных:\n"
            prompt += json.dumps(context, ensure_ascii=False, indent=2)

            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Вы - юридический ассистент. Создайте юридический документ по предоставленному шаблону и данным."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=2000
            )

            document_content = response.choices[0].message.content

            self._cache_response(cache_key, document_content)
            logger.info("Document successfully generated and cached.")
            return document_content

        except Exception as e:
            logger.error(f"Error generating document: {e}", exc_info=True)
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
