"""
WSGI config for GameSmashrooms project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
import cloudinary

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GameSmashrooms.settings')

cloudinary.config(
    cloud_name='de64coy5w',
    api_key='637756129325518',
    api_secret='lvBRQjMSCJgC9GmRbZNEWqQd03c'
)


application = get_wsgi_application()

app = application