from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def health_check(request):
    return Response({
        'status': 'healthy',
        'service': 'MediCheck API',
        'version': '1.0.0',
        'database': 'connected' if check_db() else 'disconnected'
    })

def check_db():
    from django.db import connection
    try:
        connection.ensure_connection()
        return True
    except:
        return False