# legal_app/models.py
from django.db import models
from django.contrib.auth.models import User

class LegalQuestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Ожидает ответа'),
            ('answered', 'Отвечен'),
            ('failed', 'Ошибка')
        ],
        default='pending'
    )
    processing_time = models.FloatField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['category']),
        ]

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
    