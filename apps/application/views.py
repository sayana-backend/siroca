
from .serializers import *
from .models import *
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from apps.user.permissions import *
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

class ApplicationFormCreateAPIView(generics.CreateAPIView):
    queryset = ApplicationForm.objects.all()
    serializer_class = ApplicationFormDetailSerializer
    permission_classes = [IsAdminUser, IsManagerUser]


class ApplicationFormListAPIView(generics.ListAPIView):
    queryset = ApplicationForm.objects.all()
    serializer_class = ApplicationFormDetailSerializer
    permission_classes = [IsAuthenticated]


class ApplicationFormRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ApplicationForm.objects.all()
    serializer_class = ApplicationFormDetailSerializer
    permission_classes = [IsManagerCanEdit, IsAdminUser]
    lookup_field = 'id'

class ApplicationFormRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ApplicationForm.objects.all()
    serializer_class = ApplicationFormDetailSerializer
    permission_classes = [IsManagerCanEdit, IsAdminUser]
    lookup_field = 'id'



class ApplicationLogsListCreateAPIView(generics.ListCreateAPIView):  ### внимательно посмотреть нужен ли CREATE - запрос
    queryset = ApplicationLogs.objects.all()
    serializer_class = ApplicationLogsSerializer
    permission_classes = [IsClientCanViewLogs, IsAdminUser, IsManagerUser]


# class ApplicationLogsRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):   #### убрать DELETE - запрос
#     queryset = ApplicationLogs.objects.all()
#     serializer_class = ApplicationLogsSerializer
#     lookup_field = 'id'


class ChecklistAPIView(generics.ListCreateAPIView):
    queryset = Checklist.objects.all()
    serializer_class = ChecklistSerializer
    permission_classes = [IsClientCanAddChecklist, IsAdminUser, IsManagerUser]


class CheckListDetailAPIView(generics.RetrieveUpdateDestroyAPIView):   ### посмотреть внимательно
    queryset = Checklist.objects.all()
    serializer_class = ChecklistSerializer
    lookup_field = 'id'
    permission_classes = [IsAdminUser, IsManagerUser]


class CommentsAPIView(generics.ListCreateAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = [IsClientCanPutComments, IsAdminUser, IsManagerUser]


class CommentsDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    lookup_field = 'id'
    permission_classes = [IsManagerCanEdit, IsClientCanPutComments, IsClientCanDeleteComments, IsAdminUser, IsManagerUser]


class NotificationAPIView(generics.ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_superuser:
            admin_notifications = Notification.objects.filter(is_admin=True)
            serializer = NotificationSerializer(admin_notifications, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            user_application = ApplicationForm.objects.filter(Q(main_client=request.user) | Q(main_manager=request.user))
            notification_user_application = Notification.objects.filter(form__in=user_application)
            serializer = NotificationSerializer(notification_user_application, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
