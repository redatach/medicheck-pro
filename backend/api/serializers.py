# api/serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import SymptomCheck, Disease, ChatConversation, ChatMessage
import base64
from django.core.files.base import ContentFile

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone', 'is_doctor']
        read_only_fields = ['id']

class SymptomCheckSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    photo_url = serializers.SerializerMethodField()
    
    class Meta:
        model = SymptomCheck
        fields = [
            'id', 'user', 'description', 'age', 'gender', 
            'photo', 'photo_url', 'predicted_diseases', 'urgency_level',
            'confidence_score', 'recommendations', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'predicted_diseases', 'urgency_level', 
                           'confidence_score', 'recommendations']
    
    def get_photo_url(self, obj):
        if obj.photo:
            return obj.photo.url
        return None
    
    def create(self, validated_data):
        # Analyse IA simulée
        validated_data['predicted_diseases'] = ['Grippe', 'Rhume', 'Allergie']
        validated_data['urgency_level'] = 'medium'
        validated_data['confidence_score'] = 0.78
        validated_data['recommendations'] = """
        1. Reposez-vous bien
        2. Hydratez-vous régulièrement
        3. Prenez un antipyrétique si fièvre > 38.5°C
        4. Consultez un médecin si les symptômes persistent plus de 3 jours
        """
        
        return super().create(validated_data)

class DiseaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disease
        fields = '__all__'

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'is_user', 'content', 'created_at']
        read_only_fields = ['id', 'created_at']

class ChatConversationSerializer(serializers.ModelSerializer):
    messages = ChatMessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = ChatConversation
        fields = ['id', 'symptom_check', 'messages', 'created_at']
        read_only_fields = ['id', 'created_at']

# Serializer pour l'analyse avec photo en base64
class SymptomAnalysisSerializer(serializers.Serializer):
    description = serializers.CharField(required=True)
    age = serializers.IntegerField(min_value=0, max_value=120, required=True)
    gender = serializers.ChoiceField(choices=['male', 'female', 'other'], required=True)
    photo_base64 = serializers.CharField(required=False, allow_blank=True)
    
    def create(self, validated_data):
        photo_base64 = validated_data.pop('photo_base64', None)
        symptom_check = SymptomCheck(**validated_data)
        
        if photo_base64:
            format, imgstr = photo_base64.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=f'photo.{ext}')
            symptom_check.photo = data
        
        # Analyse IA
        symptom_check.predicted_diseases = ['Grippe', 'Rhume']
        symptom_check.urgency_level = 'medium'
        symptom_check.confidence_score = 0.82
        symptom_check.recommendations = """
        1. Prenez votre température
        2. Reposez-vous
        3. Buvez beaucoup d'eau
        """
        
        symptom_check.save()
        return symptom_check