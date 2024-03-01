from apps.application.serializers import ApplicationFormFilterSerializer
from django_filters.rest_framework import DjangoFilterBackend
from apps.application.models import ApplicationForm
from report.filters import ApplicationFormFilter
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework import viewsets
from datetime import datetime
import pandas as pd
import platform
import string
import random
import os


# class ApplicationFormFilterAPIView(viewsets.GenericViewSet):
class ApplicationFormFilterAPIView(viewsets.ReadOnlyModelViewSet):
    queryset = ApplicationForm.objects.all()
    serializer_class = ApplicationFormFilterSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ApplicationFormFilter

    # def list(self, request, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)


class ExportToExcelView(APIView):
    def get_desktop_path(self):
        system = platform.system()
        if system == 'Windows':
            desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Documents')
        elif system == 'Darwin':  # macOS
            desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        elif system == 'Linux':
            desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        else:
            desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        return desktop_path

    def generate_random_string(self, length=6):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))

    def get(self, request, *args, **kwargs):
        queryset = ApplicationForm.objects.all()
        queryset = ApplicationFormFilter(request.GET, queryset=queryset).qs
        serializer = ApplicationFormFilterSerializer(queryset, many=True)
        data = serializer.data

        df = pd.DataFrame(data)
        date_str = datetime.now().strftime('%Y-%m-%d')
        random_suffix = self.generate_random_string()
        filename = f"siroco_{date_str}_report_{random_suffix}.xlsx"
        desktop_path = self.get_desktop_path()
        excel_file_path = os.path.join(desktop_path, filename)
        df.to_excel(excel_file_path, index=False, na_rep="нет значения")

        file_size = os.path.getsize(excel_file_path)

        if os.path.exists(excel_file_path):
            os.startfile(excel_file_path)
            return HttpResponse(f"Файл успешно скачан и открыт. Размер файла в байтах: {file_size} байт")
        else:
            return HttpResponse("Не удалось открыть файл")
