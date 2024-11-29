from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
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
                
                # Ensure response is a dictionary with keys
                if 'answer' in response and 'category' in response:
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
                else:
                    return format_russian_response({
                        'status': 'error',
                        'message': 'Не удалось получить правильный ответ от AI.'
                    }, status=500)
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
