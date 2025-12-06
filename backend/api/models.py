# api/models.py - COMPLET AVEC TOUT LE MODÈLE

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
import uuid

# Custom User Model
class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    is_doctor = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'users'

class SymptomCheck(models.Model):
    """Diagnostic avec texte libre et photo"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='diagnostics', null=True, blank=True)
    
    # Partie TEXTE
    description = models.TextField(verbose_name="Description des symptômes")
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=[
        ('male', 'Homme'),
        ('female', 'Femme'),
        ('other', 'Autre'),
    ])
    
    # Partie PHOTO
    photo = models.ImageField(
        upload_to='symptom_photos/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name="Photo du symptôme",
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'heic'])]
    )
    
    # Résultats
    predicted_diseases = models.JSONField(default=list)  # Liste des maladies possibles
    urgency_level = models.CharField(max_length=20)  # faible/medium/high/emergency
    confidence_score = models.FloatField()  # Confiance du modèle
    recommendations = models.TextField()  # Recommandations personnalisées
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        db_table = 'symptom_checks'
    
    def __str__(self):
        return f"Diagnostic {self.id} - {self.get_urgency_display()}"
    
    def get_urgency_display(self):
        urg = {
            'low': '🟢 Faible',
            'medium': '🟡 Moyenne', 
            'high': '🟠 Élevée',
            'emergency': '🔴 Urgence'
        }
        return urg.get(self.urgency_level, self.urgency_level)

class Disease(models.Model):
    """Base de connaissances des maladies"""
    name = models.CharField(max_length=200, unique=True)
    icd_code = models.CharField(max_length=10, blank=True)  # Code ICD-10
    description = models.TextField()
    symptoms = models.JSONField(default=list)  # Liste des symptômes
    common_ages = models.CharField(max_length=100, blank=True)
    gender_prevalence = models.CharField(max_length=50, blank=True)
    urgency_level = models.CharField(max_length=20)
    treatment = models.TextField(blank=True)
    when_to_see_doctor = models.TextField()
    prevention_tips = models.TextField(blank=True)
    
    class Meta:
        db_table = 'diseases'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.icd_code})"

class ChatConversation(models.Model):
    """Conversation avec l'IA médicale"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    symptom_check = models.ForeignKey(SymptomCheck, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'chat_conversations'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Conversation {self.id}"

class ChatMessage(models.Model):
    """Message dans une conversation"""
    conversation = models.ForeignKey(ChatConversation, on_delete=models.CASCADE, related_name='messages')
    is_user = models.BooleanField(default=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'chat_messages'
        ordering = ['created_at']
    
    def __str__(self):
        prefix = "User" if self.is_user else "AI"
        return f"{prefix}: {self.content[:50]}"