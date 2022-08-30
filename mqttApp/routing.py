from django.urls import path
from .consumers import MqttConsumer



ws_urlPatterns=[
 path('ws/url/',MqttConsumer.as_asgi())

]