from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from .models import *
from django.shortcuts import get_object_or_404
from django.core import serializers
from asgiref.sync import sync_to_async

# class ControlPanelConsumer(AsyncWebsocketConsumer):
#     async def connect(self):

#         # Check if the user is connected to a WebSocket
#         if self.scope["user"].is_authenticated and self.scope["user"].is_active:
#             await self.accept()
#             print('Connected')

#         else:
#             # User is not connected to a WebSocket
#             # You can choose to reject the connection or handle it differently
#             await self.close()
            
#     async def disconnect(self, close_code):
#         print('Disconnected')
        
class ControlPanelConsumer(AsyncWebsocketConsumer): 
    async def connect(self):
        if self.scope["user"].is_authenticated and self.scope["user"].is_active:
            event_slug = self.scope['url_route']['kwargs']['event_slug']
            kategori_slug = self.scope['url_route']['kwargs']['kategori_slug']
            jenis_kelamin = self.scope['url_route']['kwargs']['jenis_kelamin']
            bagan_pk = self.scope['url_route']['kwargs']['bagan_pk']
            detailbagan_pk = self.scope['url_route']['kwargs']['detailbagan_pk']
            tatami_pk = self.scope['url_route']['kwargs']['tatami_pk']
            
            self.event_slug = event_slug
            self.kategori_slug = kategori_slug
            self.jenis_kelamin = jenis_kelamin
            self.bagan_pk = bagan_pk
            self.detailbagan_pk = detailbagan_pk
            self.tatami_pk = tatami_pk
            
            self.room_group_name = f'ring_{tatami_pk}_{detailbagan_pk}'
            
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()
            
        else:
            await self.close()
            
    async def disconnect(self, close_code):
        print(f'Disconnected {close_code}')
        
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )
        
    async def sendscore(self, event):
        message1 = event['message1']
        message2 = event['message2']
        sender = event['sender']
        valid = event['valid']
        
        await self.send(text_data=json.dumps({
            'message1': message1,
            'message2': message2,
            'sender': sender,
            'valid': valid,
        }))
        
    
class DashboardConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        dashboard_slug = self.scope['url_route']['kwargs']['dashboard_slug']
        self.dashboard_slug = dashboard_slug
        self.room_group_name = f'stats-{dashboard_slug}'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        print(f'connection closed with code: {close_code}')
        
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        sender = text_data_json["sender"]
        
        print(message)
        print(sender)
        
        dashboard_slug = self.dashboard_slug
        
        await self.save_data_item(sender, message, dashboard_slug)
        
        await self.channel_layer.group_send(self.room_group_name, {
            'type': 'statistics_message',
            'message': message,
            'sender': sender,
        })
        
    async def statistics_message(self, event):
        message = event['message']
        sender = event['sender']
        
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
        }))
        
    @database_sync_to_async
    def create_data_item(self, sender, message, slug):
        obj = Statistic.objects.get(slug=slug)
        return DataItem.objects.create(statistic=obj, value=message, owner=sender)
    
    async def save_data_item(self, sender, message, slug):
        await self.create_data_item(sender, message, slug)