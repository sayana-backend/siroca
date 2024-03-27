import json
import jwt
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Notification
import datetime
from channels.db import database_sync_to_async
import logging

logger = logging.getLogger(__name__)

# latest_notification = Notification.objects.latest('created_at')
# latest_notification = Notification.objects.all()
# notification_message = {
#     "task_number": latest_notification.task_number,
#     "title": latest_notification.title,
#     "text": latest_notification.text,
#     "created_at": str(latest_notification.created_at),
#     "made_change": latest_notification.made_change if latest_notification.made_change else None,
# }
#
#
# class NotificationConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()
#         await self.channel_layer.group_add("notifications", self.channel_name)
#         await self.send(text_data="Привет! Вы успешно подключились к WebSocket.")
#
#         await self.send(text_data=json.dumps(notification_message, ensure_ascii=False))
#
#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard("notifications", self.channel_name)
#
#     async def send_notification(self, event):
#         message = event["message"]
#
#         await self.send(
#             text_data=json.dumps(
#                 message, ensure_ascii=False
#             )
#         )

# class NotificationConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()
#         await self.channel_layer.group_add("notifications", self.channel_name)
#
#         # Проверяем, существует ли ключ 'last_disconnect_time' в сессии
#         last_disconnect_time = await sync_to_async(self.scope['session'].get)('last_disconnect_time', None)
#         if not last_disconnect_time:
#             # Если ключ не существует, устанавливаем его в текущее время
#             last_disconnect_time = datetime.datetime.now()
#             await sync_to_async(self.scope['session'].__setitem__)('last_disconnect_time', last_disconnect_time)
#
#         # Получаем уведомления из базы данных, которые были созданы во время отключения
#         notifications = await sync_to_async(Notification.objects.filter)(created_at__gte=last_disconnect_time)
#
#         # Отправляем уведомления
#         for notification in notifications:
#             await self.send(
#                 text_data=json.dumps(
#                     {
#                         "task_number": notification.task_number,
#                         "title": notification.title,
#                         "text": notification.text,
#                         "created_at": str(notification.created_at),
#                         "made_change": notification.made_change.first_name if notification.made_change else None,
#                     },
#                     ensure_ascii=False
#                 )
#             )
#
#         # Удаляем уведомления из базы данных
#         await sync_to_async(notifications.delete)()
#
#     async def disconnect(self, close_code):
#         last_disconnect_time = datetime.datetime.now()
#         await sync_to_async(self.scope['session'].__setitem__)('last_disconnect_time', last_disconnect_time)
#         await self.channel_layer.group_discard("notifications", self.channel_name)
#
#     async def send_notification(self, event):
#         message = event["message"]
#
#         await self.send(
#             text_data=json.dumps(
#                 message, ensure_ascii=False
#             )
#         )

# class NotificationConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()
#         await self.channel_layer.group_add("notifications", self.channel_name)
#
#         # Используем sync_to_async для асинхронного получения уведомлений
#         notifications = await sync_to_async(Notification.objects.all)()
#         notification_ids = [notification.id for notification in notifications]
#         for notification in notifications:
#             await self.send_notification({"message": model_to_dict(notification)})
#
#         # Удаляем уведомления после отправки
#         await sync_to_async(Notification.objects.filter(id__in=notification_ids).delete)()
#
#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard("notifications", self.channel_name)
#
#     async def send_notification(self, event):
#         message = event["message"]
#
#         await self.send(
#             text_data=json.dumps(
#                 message, ensure_ascii=False
#             )
#         )


# class NotificationConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()
#         await self.channel_layer.group_add("notifications", self.channel_name)
#
#         # При подключении клиента отправить ему все уведомления из базы данных
#         notifications = await database_sync_to_async(Notification.objects.all)()
#         for notification in notifications:
#             await self.send_notification(notification)
#
#     async def send_notification(self, notification):
#         message = {
#             "task_number": notification.task_number,
#             "title": notification.title,
#             "text": notification.text,
#             "created_at": str(notification.created_at),
#             "made_change": notification.made_change.first_name if notification.made_change else None,
#         }
#
#         await self.send(
#             text_data=json.dumps(
#                 message, ensure_ascii=False
#             )
#         )
#
#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard("notifications", self.channel_name)

# class NotificationConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()
#         await self.send_notifications()
#
#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard("notifications", self.channel_name)
#
#     async def send_notifications(self):
#         notifications = await self.get_notifications()
#         for notification in notifications:
#             await self.send(text_data=json.dumps({
#                 'task_number': notification.task_number,
#                 'title': notification.title,
#                 'text': notification.text,
#                 'created_at': str(notification.created_at),
#                 'made_change': notification.made_change.first_name if notification.made_change else None
#             }))


# class NotificationConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.user = self.scope["user"]
#         self.user_id = self.user.id
#
#         logger.info(f"Connected user ID: {self.user_id}")
#
#         await self.accept()
#         await self.channel_layer.group_add("notifications", self.channel_name)
#
#         notifications = await self.get_notifications()
#         for notification in notifications:
#             await self.send_notification(notification)
#
#     async def disconnect(self, close_code):
#         logger.info(f"Disconnected user ID: {self.user_id}")
#
#         await self.channel_layer.group_discard("notifications", self.channel_name)
#
#     async def send_notification(self, notification):
#         await self.send(
#             text_data=json.dumps({
#                 'task_number': notification.task_number,
#                 'title': notification.title,
#                 'text': notification.text,
#                 'created_at': str(notification.created_at),
#                 'made_change': notification.made_change.first_name if notification.made_change else None
#             })
#         )
#
#     @database_sync_to_async
#     def get_notifications(self):
#         return Notification.objects.all()


# class NotificationConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()
#         await self.channel_layer.group_add("notifications", self.channel_name)
#         await self.send(text_data="Привет! Вы успешно подключились к WebSocket.")
#         notifications = Notification.objects.all()
#         for notification in notifications:
#             await self.send_notification(notification)
#
#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard("notifications", self.channel_name)
#
#     async def send_notification(self, notification):
#         message = {
#             "task_number": notification.task_number,
#             "title": notification.title,
#             "text": notification.text,
#             "created_at": str(notification.created_at),
#             "made_change": notification.made_change.first_name if notification.made_change else None,
#         }
#         await self.send(text_data=json.dumps(message, cls=DjangoJSONEncoder))

# class NotificationConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()
#         await self.channel_layer.group_add("notifications", self.channel_name)
#         await self.send(text_data="Привет! Вы успешно подключились к WebSocket.")

        # Отправка всех уведомлений при подключении
        # all_notifications = await sync_to_async(list)(Notification.objects.all())
        # for notification in all_notifications:
        #     await self.send_notification(notification)
    #     all_notifications = await sync_to_async(list)(Notification.objects.all())
    #     for notification_data in all_notifications:
    #         notification = Notification(**notification_data)
    #         await self.send_notification(notification)
    #
    # async def disconnect(self, close_code):
    #     await self.channel_layer.group_discard("notifications", self.channel_name)

    # async def send_notification(self, notification):
    #     await self.send(text_data=json.dumps({
    #         "task_number": notification.task_number,
    #         "title": notification.title,
    #         "text": notification.text,
    #         "created_at": str(notification.created_at),
    #         "made_change": notification.made_change if notification.made_change else None,
    #     }, ensure_ascii=False))

    # async def send_notification(self, notification):
    #     await self.send(text_data=json.dumps({
    #         "task_number": notification.task_number,
    #         "title": notification.title,
    #         "text": notification.text,
    #         "created_at": str(notification.created_at),
    #         "made_change": notification.made_change if notification.made_change else None,
    #     }, ensure_ascii=False))

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("notifications", self.channel_name)
        await self.send(text_data="Привет! Вы успешно подключились к WebSocket.")

        # Отправка всех уведомлений при подключении
        all_notifications = await sync_to_async(list)(Notification.objects.all())
        for notification in all_notifications:
            await self.send_notification(notification)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("notifications", self.channel_name)

    # async def send_notification(self, notification):
    #     await self.send(text_data=json.dumps({
    #         "task_number": notification.task_number,
    #         "title": notification.title,
    #         "text": notification.text,
    #         "created_at": str(notification.created_at),
    #         "made_change": notification.made_change if notification.made_change else None,
    #     }, ensure_ascii=False))

    # async def send_notification(self, notification):
    #     await self.send(text_data=json.dumps({
    #         "task_number": notification["task_number"],
    #         "title": notification["title"],
    #         "text": notification["text"],
    #         "created_at": str(notification["created_at"]),
    #         "made_change": notification["made_change"] if "made_change" in notification else None,
    #     }, ensure_ascii=False))

    async def send_notification(self, notification):
        notification = {
            "task_number": notification.task_number,
            "title": notification.title,
            "text": notification.text,
            "created_at": str(notification.created_at),
            "made_change": notification.made_change if notification.made_change else None,
        }
        await self.send(text_data=json.dumps(notification, ensure_ascii=False))
