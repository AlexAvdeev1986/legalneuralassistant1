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
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core.validators import validate_ipv46_address
from django_ratelimit.decorators import ratelimit
from django.shortcuts import get_object_or_404
from .forms import LegalQuestionForm, DocumentGeneratorForm
from .models import LegalQuestion, Document  # Ensure Document is imported
from .utils import LegalAI
import logging
import json
from functools import wraps
from docx import Document as DocxDocument
from typing import Dict, Any

# Initialize LegalAI instance and logger
legal_ai = LegalAI()
logger = logging.getLogger(__name__)

def format_russian_response(data: Dict[str, Any], status: int = 200) -> JsonResponse:
    """Formats a JSON response supporting Russian language."""
    return JsonResponse(data, json_dumps_params={'ensure_ascii': False}, status=status)

@ensure_csrf_cookie
def home(request):
    """Renders the home page."""
    return render(request, 'legal_app/home.html', {
        'title': 'Главная страница',
        'description': 'Юридический помощник с искусственным интеллектом'
    })

def handle_errors(view_func):
    """Decorator for handling common errors in views with Russian messages."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        try:
            return view_func(request, *args, **kwargs)
        except ValidationError as e:
            logger.warning(f"Validation error: {str(e)}")
            return format_russian_response({'status': 'error', 'message': 'Ошибка валидации данных.'}, 400)
        except json.JSONDecodeError as e:
            logger.warning(f"JSON decode error: {str(e)}")
            return format_russian_response({'status': 'error', 'message': 'Некорректный формат JSON.'}, 400)
        except Exception as e:
            logger.error(f"Internal error: {str(e)}", exc_info=True)
            return format_russian_response({'status': 'error', 'message': 'Произошла внутренняя ошибка сервера.'}, 500)
    return wrapper

def get_client_ip(request) -> str:
    """Retrieve and validate the client IP address."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    ip = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')
    
    try:
        validate_ipv46_address(ip)
        return ip
    except ValidationError:
        return 'unknown'

@login_required
@require_http_methods(["GET", "POST"])
@ratelimit(key='user', rate='10/m', group='legal_chat')
@handle_errors
def chat(request):
    """Handle legal chat interactions and generate responses."""
    if request.method == 'POST':
        if getattr(request, 'limited', False):
            return format_russian_response({'status': 'error', 'message': 'Превышен лимит запросов. Подождите минуту.'}, 429)
        
        form = LegalQuestionForm(request.POST)
        if form.is_valid():
            question = form.cleaned_data['question']
            user_ip = get_client_ip(request)
            
            response = legal_ai.get_legal_response(question)
            if response.get('status') == 'success':
                legal_question = LegalQuestion.objects.create(
                    user=request.user,
                    question=question,
                    answer=response['answer'],
                    category=response['category'],
                    ip_address=user_ip,
                    status='answered'
                )
                return format_russian_response({
                    'status': 'success',
                    'answer': response['answer'],
                    'category': response['category'],
                    'question_id': legal_question.id
                })
            else:
                return format_russian_response({'status': 'error', 'message': 'Не удалось получить ответ от AI.'}, 500)
        
        return format_russian_response({'status': 'error', 'errors': form.errors}, 400)

    # GET request: display form and question history
    questions = LegalQuestion.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'legal_app/chat.html', {'form': LegalQuestionForm(), 'questions': questions})

@login_required
@require_http_methods(["GET", "POST"])
@handle_errors
def document_generator(request):
    """Generate legal documents dynamically."""
    if request.method == 'POST':
        form = DocumentGeneratorForm(request.POST)
        if form.is_valid():
            try:
                doc_type = form.cleaned_data['document_type']
                title = form.cleaned_data['title']
                context = form.cleaned_data['context']  # Direct plain text context
                
                # Generate document using LegalAI
                generated_content = legal_ai.generate_document(doc_type, context)
                
                # Create Word document
                document = DocxDocument()
                document.add_heading(title, 0)
                for paragraph in generated_content.split("\n"):
                    document.add_paragraph(paragraph)
                
                # Prepare document for download
                response = HttpResponse(
                    content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
                )
                response['Content-Disposition'] = f'attachment; filename="{title}.docx"'
                document.save(response)
                
                logger.info(f"Document '{title}' generated successfully.")
                return response
            
            except Exception as e:
                logger.error(f"Error generating document: {str(e)}", exc_info=True)
                return format_russian_response({'status': 'error', 'message': 'Ошибка при генерации документа.'}, 500)
        
        return format_russian_response({'status': 'error', 'errors': form.errors}, 400)

    # GET request: display form and document history
    documents = Document.objects.filter(user=request.user).order_by('-created_at')  # Ensure Document is defined
    return render(request, 'legal_app/document_generator.html', {
        'form': DocumentGeneratorForm(),
        'documents': documents  # Ensure 'documents' context is passed for history display
    })

def download_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    response = HttpResponse(document.file, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = f'attachment; filename="{document.title}.docx"'
    return response



    ├── forms.py
# legal_app/forms.py
from django import forms
from .models import LegalQuestion, Document

class LegalQuestionForm(forms.ModelForm):
    class Meta:
        model = LegalQuestion
        fields = ['question']
        widgets = {
            'question': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'Введите ваш юридический вопрос...'
            })
        }

class DocumentGeneratorForm(forms.Form):
    document_type = forms.ChoiceField(
        choices=[
            ('complaint', 'Жалоба'),
            ('contract', 'Договор'),
            ('statement', 'Заявление'),
            ('pretension', 'Претензия'),
        ],
        label='Тип документа',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    title = forms.CharField(
        label='Название',
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    context = forms.CharField(
        label='Контекст',
        widget=forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
        help_text='Введите контекст документа.'
    )
    
    content = forms.CharField(
        label='Содержание документа',
        widget=forms.Textarea(attrs={'rows': 8, 'class': 'form-control', 'placeholder': 'Введите содержание документа'}),
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
        self.cache_timeout = 3600  # 1 hour cache timeout

    def _get_cached_response(self, cache_key: str) -> Any:
        """Retrieve a response from the cache."""
        return cache.get(cache_key)

    def _cache_response(self, cache_key: str, response: Any):
        """Store a response in the cache."""
        cache.set(cache_key, response, self.cache_timeout)

    def get_legal_response(self, question: str) -> Dict[str, Any]:
        """Get a legal response to a user's question from OpenAI."""
        start_time = time.time()
        cache_key = f"legal_response_{hash(question)}"

        # Check if response is cached
        cached_response = self._get_cached_response(cache_key)
        if cached_response:
            logger.info("Response found in cache.")
            return cached_response

        try:
            # Generate the legal answer and its category
            answer = self._get_openai_response(question, context_type="answer")
            category = self._get_openai_response(question, context_type="category")

            # Format the legal response
            formatted_response = self._format_response(answer, category)

            # Cache the result
            self._cache_response(cache_key, formatted_response)
            logger.info("Response successfully generated and cached.")
            return formatted_response

        except Exception as e:
            logger.error(f"Error processing request: {e}", exc_info=True)
            return self._handle_error(e, start_time)

    def _get_openai_response(self, question: str, context_type: str) -> str:
        """Get a legal answer or category from OpenAI."""
        if context_type == "answer":
            system_message = "You are a legal assistant providing accurate and relevant legal information under Russian law."
        else:
            system_message = "Determine the category of this legal question (e.g., civil law, criminal law, administrative law)."

        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": question},
            ],
            temperature=0.5 if context_type == "answer" else 0.3,
            max_tokens=2000 if context_type == "answer" else 100,
        )
        return response.choices[0].message.content.strip()

    def _format_response(self, answer: str, category: str) -> Dict[str, Any]:
        """Format the legal response with status and details."""
        return {
            "status": "success",
            "category": category,
            "answer": answer,
            "formatted_answer": f"**Category:** {category}\n\n**Answer:**\n{answer}",
        }

    def _handle_error(self, error: Exception, start_time: float) -> Dict[str, Any]:
        """Handle errors by logging and returning a generic error response."""
        elapsed_time = time.time() - start_time
        return {
            "status": "error",
            "message": "An error occurred while processing your request. Please try again later.",
            "details": str(error),
            "processing_time": elapsed_time,
        }

    def generate_document(self, doc_type: str, context: str) -> str:
        """Generate a legal document based on the given context."""
        # Cache key based on document type and context (now plain text)
        cache_key = f"document_{hash(doc_type)}_{hash(context)}"

        # Check if the document is cached
        cached_document = self._get_cached_response(cache_key)
        if cached_document:
            logger.info("Document found in cache.")
            return cached_document

        try:
            # Generate document content using OpenAI
            document_content = self._generate_document_content(doc_type, context)

            # Cache the document content
            self._cache_response(cache_key, document_content)
            logger.info("Document successfully generated and cached.")
            return document_content

        except Exception as e:
            logger.error(f"Error generating document: {e}", exc_info=True)
            return f"Error generating document: {str(e)}"

    def _generate_document_content(self, doc_type: str, context: str) -> str:
        """Generate a legal document using OpenAI based on the context."""
        prompt = f"Create a {doc_type} based on the following details:\n"
        prompt += context  # Now it's plain text instead of JSON

        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a legal assistant. Create a legal document based on the provided template and details.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.5,
            max_tokens=2000,
        )
        return response.choices[0].message.content.strip()


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
    <!-- Form Section -->
    <div class="col-md-8">
        <div class="card">
            <div class="card-header">
                <h5 class="card-title mb-0">Генератор документов</h5>
            </div>
            <div class="card-body">
                <form id="documentForm" method="post">
                    {% csrf_token %}
                    <!-- Render the form fields using crispy_forms for better formatting -->
                    {{ form|crispy }}

                    <!-- Submit button for document generation -->
                    <button type="submit" class="btn btn-primary">Создать документ</button>
                </form>

                <!-- Display form errors if any -->
                {% if form.errors %}
                    <div class="alert alert-danger mt-3">
                        <strong>Ошибки формы:</strong>
                        <ul>
                            {% for field, errors in form.errors.items %}
                                <li>{{ field }}: {{ errors|join:", " }}</li>
                            {% endfor %}
                        </ul>
                    </div>
                {% endif %}
            </div>
        </div>
    </div>

    <!-- Document History Section -->
    <div class="col-md-4">
        <div class="card">
            <div class="card-header">
                <h5 class="card-title mb-0">История документов</h5>
            </div>
            <div class="card-body">
                {% if documents %}
                    <!-- Display the list of generated documents -->
                    <div class="list-group">
                        {% for document in documents %}
                            <a href="{% url 'download_document' document.id %}" class="list-group-item list-group-item-action">
                                {{ document.title }} - {{ document.document_type }} <br>
                                <small>{{ document.created_at|date:"d.m.Y H:i" }}</small>
                            </a>
                        {% endfor %}
                    </div>
                {% else %}
                    <!-- Message when there are no documents in history -->
                    <p class="text-muted">История документов отсутствует.</p>
                {% endif %}
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
