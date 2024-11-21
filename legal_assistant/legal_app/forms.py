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
