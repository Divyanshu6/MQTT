"""
ASGI config for mqttProject project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
import websockets
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from mqttApp.routing import ws_urlPatterns 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mqttProject.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket":AuthMiddlewareStack(URLRouter(ws_urlPatterns)),

})