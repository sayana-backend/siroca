from .models import ApplicationForm, Checklist, Comments, ApplicationLogs
from .serializers import (ApplicationFormDetailSerializer,
                          ChecklistSerializer,
                          CommentsSerializer,
                          ApplicationLogsSerializer)
from rest_framework import generics
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ApplicationFormFilter
from datetime import datetime


class ApplicationFormCreateAPIView(generics.CreateAPIView):
    queryset = ApplicationForm.objects.all()
    serializer_class = ApplicationFormDetailSerializer


class ApplicationFormListAPIView(generics.ListAPIView):
    serializer_class = ApplicationFormDetailSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ApplicationFormFilter
    def get_queryset(self):
        user = self.request.user
        search_query = self.request.query_params.get('search', None)
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
            
            if search_query:
                start_date, end_date = None, None
                if "-" in search_query:
                    start_str, end_str = search_query.split("-")
                    start_date = datetime.strptime(start_str.strip(), "%Y-%m-%d")
                    end_date = datetime.strptime(end_str.strip(), "%Y-%m-%d")
                queryset = queryset.filter(
                    Q(task_number__icontains=search_query) |
                    Q(title__icontains=search_query) |
                    Q(description__icontains=search_query) |
                    Q(main_client__first_name__icontains=search_query) |
                    Q(main_manager__first_name__icontains=search_query) |
                    Q(priority__icontains=search_query) |
                    Q(payment_state__icontains=search_query)
                )
                if start_date and end_date:
                    queryset = queryset.filter(start_date__gte=start_date, finish_date__lte=end_date)
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







