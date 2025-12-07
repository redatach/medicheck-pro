"""
WSGI config for medicheck project.

It exposes the WSGI callable as a module-level variable named ``application``.
"""

import os
import sys

# Ajoutez le chemin du projet au sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medicheck.settings')

application = get_wsgi_application()
