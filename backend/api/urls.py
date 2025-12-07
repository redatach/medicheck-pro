from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'diagnostics', views.SymptomCheckViewSet, basename='diagnostic')
router.register(r'diseases', views.DiseaseViewSet, basename='disease')
router.register(r'chat', views.ChatConversationViewSet, basename='chat')


urlpatterns = [
    path('', include(router.urls)),
    path('health/', views.health_check, name='health'),
    path('quick-analysis/', views.quick_analysis, name='quick-analysis'),
    path('register/', views.register, name='register'),
]
