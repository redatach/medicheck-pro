from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, status
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.db import connection


# -------------------------------------------------------------------
# ✔ HEALTH CHECK
# -------------------------------------------------------------------
@api_view(['GET'])
def health_check(request):
    return Response({
        'status': 'healthy',
        'service': 'MediCheck API',
        'version': '1.0.0',
        'database': 'connected' if check_db() else 'disconnected'
    })


def check_db():
    try:
        connection.ensure_connection()
        return True
    except:
        return False


# -------------------------------------------------------------------
# ✔ REGISTER ENDPOINT (auth simple)
# -------------------------------------------------------------------
@api_view(['POST'])
def register(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response({"error": "username and password required"}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({"error": "User already exists"}, status=400)

    user = User.objects.create(
        username=username,
        password=make_password(password)
    )

    return Response({"message": "User created", "user_id": user.id})


# -------------------------------------------------------------------
# ✔ QUICK ANALYSIS (mini diagnostic)
# -------------------------------------------------------------------
@api_view(['POST'])
def quick_analysis(request):
    symptoms = request.data.get("symptoms", [])

    if not symptoms:
        return Response({"error": "No symptoms provided"}, status=400)

    return Response({
        "input": symptoms,
        "diagnostic": "Probabilité faible d'infection",
        "urgency": "low"
    })


# -------------------------------------------------------------------
# ✔ VIEWSET 1 : SymptomCheckViewSet
# -------------------------------------------------------------------
class SymptomCheckViewSet(viewsets.ViewSet):
    def create(self, request):
        symptoms = request.data.get("symptoms", [])
        if not symptoms:
            return Response({"error": "No symptoms provided"}, status=400)

        return Response({
            "symptoms_received": symptoms,
            "prediction": "Example disease",
            "urgency": "medium"
        })


# -------------------------------------------------------------------
# ✔ VIEWSET 2 : DiseaseViewSet
# -------------------------------------------------------------------
class DiseaseViewSet(viewsets.ViewSet):
    def list(self, request):
        diseases = [
            {"name": "Grippe", "symptoms": ["fièvre", "toux", "fatigue"]},
            {"name": "COVID-19", "symptoms": ["fièvre", "perte odorat", "toux"]},
        ]
        return Response(diseases)


# -------------------------------------------------------------------
# ✔ VIEWSET 3 : ChatConversationViewSet
# -------------------------------------------------------------------
class ChatConversationViewSet(viewsets.ViewSet):
    def create(self, request):
        message = request.data.get("message", "")
        if not message:
            return Response({"error": "message required"}, status=400)

        reply = f"AI Response: Vous avez dit → {message}"

        return Response({"reply": reply})
