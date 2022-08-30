from requests import request
from paho.mqtt import client as mqtt_client
import random
import time
import json
from channels.layers import get_channel_layer
import os
from asgiref.sync import async_to_sync
from django.core.cache import cache
import redis
from datetime import datetime

r = redis.Redis()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mqttProject.settings")
channel_layer = get_channel_layer()

def send_message_to_group(msg):
    async_to_sync(channel_layer.group_send)(
            "mqtt",
            {
                "type": "chat.message",
                "text": str(msg.payload.decode('utf8')),
            },
        )

def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("Connected with result code "+str(rc))
        global connected
        connected=True
    else:
        print("not connected")


def on_message(client, userdata, msg):
    recieved=True
    a=json.loads(str(msg.payload.decode('utf8')))
    b=str(msg.payload.decode('utf8'))
    #print(a['meter_address'])
    meter_address=a['meter_address']
    r.set(meter_address, b)
    print(meter_address)
    send_message_to_group(msg)

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection. rc:", rc )
        print("DISCONNECTED")


def connect_Mqtt():
    broker = "0.tcp.in.ngrok.io"
    port = 12632
    connected=False
    recieved=False
    client_id = f'python-mqtt-{random.randint(0, 100)}'
    username = "test_user"
    password = "grampower"
    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.on_message=on_message
    client.on_disconnect = on_disconnect
    client.username_pw_set(username, password)
    client.connect(broker, port)
    client.loop_start()
    client.subscribe('meter/data/#')

    while connected!=True:
        time.sleep(.2)

    while recieved!=True:
        time.sleep(.2)

    client.loop_stop()

    
