from .models import ApplicationForm, Checklist, Comments, ApplicationLogs
from .serializers import (ApplicationFormDetailSerializer,
                          ChecklistSerializer,
                          CommentsSerializer,
                          ApplicationLogsSerializer)
from rest_framework import generics
from django.db.models import Q

class ApplicationFormCreateAPIView(generics.CreateAPIView):
    queryset = ApplicationForm.objects.all()
    serializer_class = ApplicationFormDetailSerializer


class ApplicationFormListAPIView(generics.ListAPIView):
    serializer_class = ApplicationFormDetailSerializer
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_client:
                queryset = ApplicationForm.objects.filter(Q(main_client=user) | 
                                                          Q(company=user.main_company))
            elif user.is_manager:
                queryset = ApplicationForm.objects.filter(Q(main_manager=user) | 
                                                          Q(checklists__manager=user) | 
                                                          Q(company=user.main_company))
            elif user.is_superuser:
                queryset = ApplicationForm.objects.all()
            return queryset
        else:
            return ApplicationForm.objects.none()
        


class ApplicationFormRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ApplicationForm.objects.all()
    serializer_class = ApplicationFormDetailSerializer
    lookup_field = 'id'




class ApplicationLogsListCreateAPIView(generics.ListCreateAPIView):
    queryset = ApplicationLogs.objects.all()
    serializer_class = ApplicationLogsSerializer


class ApplicationLogsRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ApplicationLogs.objects.all()
    serializer_class = ApplicationLogsSerializer
    lookup_field = 'id'





class ChecklistAPIView(generics.CreateAPIView):
    queryset = Checklist.objects.all()
    serializer_class = ChecklistSerializer
    # filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    # search_fields = '__all__'
    # filterset_fields = ['completed', 'text', 'manager']


class CheckListDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Checklist.objects.all()
    serializer_class = ChecklistSerializer
    lookup_field = 'id'


class CommentsAPIView(generics.CreateAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer


class CommentsDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    lookup_field = 'id'







