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
