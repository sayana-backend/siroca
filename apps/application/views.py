from .models import ApplicationForm, Checklist, Comments, ApplicationLogs, Notification
from .serializers import (ApplicationFormDetailSerializer,
                          ChecklistSerializer,
                          CommentsSerializer,
                          ApplicationLogsSerializer,
                          NotificationSerializer)
from rest_framework import generics
from apps.user.permissions import *
from rest_framework import permissions
# from rest_framework.permissions import IsAuthenticated


class ApplicationFormCreateAPIView(generics.CreateAPIView):
    queryset = ApplicationForm.objects.all()
    serializer_class = ApplicationFormDetailSerializer
    permission_classes = [IsAdminUser,
                          IsManagerUser]


class ApplicationFormListAPIView(generics.ListAPIView):
    queryset = ApplicationForm.objects.all()
    serializer_class = ApplicationFormDetailSerializer
    permission_classes = [IsAdminUser, IsManagerUser]


class ApplicationFormRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ApplicationForm.objects.all()
    serializer_class = ApplicationFormDetailSerializer
    permission_classes = [IsManagerCanDeleteComments,
                          IsManagerCanDeleteApplication,
                          IsAdminUser]
    lookup_field = 'id'


class ApplicationLogsListCreateAPIView(generics.ListCreateAPIView):  ### внимательно посмотреть нужен ли CREATE - запрос
    queryset = ApplicationLogs.objects.all()
    serializer_class = ApplicationLogsSerializer
    permission_classes = [IsClientCanViewLogs,
                          IsAdminUser,
                          IsManagerUser]


class ApplicationLogsRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):   #### убрать DELETE - запрос
    queryset = ApplicationLogs.objects.all()
    serializer_class = ApplicationLogsSerializer
    lookup_field = 'id'


class ChecklistAPIView(generics.ListCreateAPIView):
    queryset = Checklist.objects.all()
    serializer_class = ChecklistSerializer
    permission_classes = [IsClientCanAddChecklist,
                          IsAdminUser,
                          IsManagerUser]


class CheckListDetailAPIView(generics.RetrieveUpdateDestroyAPIView):   ### посмотреть внимательно
    queryset = Checklist.objects.all()
    serializer_class = ChecklistSerializer
    lookup_field = 'id'
    permission_classes = [IsAdminUser,
                          IsManagerUser]


class CommentsAPIView(generics.ListCreateAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = [IsClientCanEditComments,
                          IsAdminUser,
                          IsManagerUser]


class CommentsDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    lookup_field = 'id'
    permission_classes = [IsManagerCanDeleteComments,
                          IsClientCanEditComments,
                          IsAdminUser]


class NotificationListAPIView(generics.ListAPIView):
    # queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    def get_queryset(self):
        user_id = self.kwargs['id']
        return Notification.objects.filter(user_id=user_id)

