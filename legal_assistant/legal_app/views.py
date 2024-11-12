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
