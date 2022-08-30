from channels.generic.websocket import WebsocketConsumer 
from django.core.cache import cache
from mqttApp.mqtt_example import connect_Mqtt,on_message
from asgiref.sync import async_to_sync
import json


class MqttConsumer(WebsocketConsumer):
    def connect(self):
        #self.username = "Anonymous"
        self.accept()
        async_to_sync(self.channel_layer.group_add)("mqtt", self.channel_name)

    def websocket_receive(self, event):
        print(event)
        # async_to_sync(self.channel_layer.group_send)(
        #     "mqtt",
        #     {
        #         "type": "chat.message",
        #         "text": "hi I'm here",
        #     },
        # )
        # print('recieved from client '+ text_data)
        # print('data recieved')
        # for i in range(20):
        #     self.send(text_data="[Welcome %s!]" % self.username)
        #     time.sleep(1)

    def chat_message(self, event):
        # data=json.loads(event['text'])
        # meter_address=data['meter_address']
        # cache.set(meter_address, event["text"])
        # print(meter_address)
        self.send(text_data=event["text"])

    def disconnect(self, message):
        print('disconnected')