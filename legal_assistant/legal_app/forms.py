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
