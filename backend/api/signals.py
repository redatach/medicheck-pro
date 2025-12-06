"""
Signaux pour MediCheck
"""

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Diagnosis, User
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Diagnosis)
def handle_critical_diagnosis(sender, instance, created, **kwargs):
    """
    Gère les diagnostics critiques
    """
    if created and instance.urgency_level in ['critical', 'high']:
        logger.info(f"Diagnostic critique détecté: {instance.id}")
        
        # Ici, vous pourriez:
        # 1. Envoyer une notification push
        # 2. Envoyer un email d'alerte
        # 3. Notifier un contact d'urgence
        
        if instance.user.email and settings.DEBUG:
            try:
                send_mail(
                    subject=f"[MediCheck] Diagnostic d'urgence - Niveau: {instance.urgency_level}",
                    message=f"""
                    Bonjour {instance.user.first_name},
                    
                    Votre diagnostic réalisé sur MediCheck indique un niveau d'urgence {instance.urgency_level}.
                    
                    Symptômes: {instance.symptoms_text[:100]}...
                    Score d'urgence: {instance.emergency_score}/10
                    
                    Recommandations immédiates:
                    {instance.immediate_actions}
                    
                    Prenez soin de vous,
                    L'équipe MediCheck
                    """,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[instance.user.email],
                    fail_silently=True,
                )
            except Exception as e:
                logger.error(f"Erreur envoi email: {str(e)}")

@receiver(pre_save, sender=User)
def normalize_user_email(sender, instance, **kwargs):
    """
    Normalise l'email de l'utilisateur
    """
    if instance.email:
        instance.email = instance.email.lower()
    
    if not instance.username and instance.email:
        instance.username = instance.email