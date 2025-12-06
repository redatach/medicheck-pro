"""
ASGI config for medicheck project.
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medicheck.settings')

application = get_asgi_application()