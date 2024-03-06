from report.serializers import ApplicationFormFilterSerializer
from django_filters.rest_framework import DjangoFilterBackend
from openpyxl.utils.dataframe import dataframe_to_rows
from apps.application.models import ApplicationForm
from report.filters import ApplicationFormFilter
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from openpyxl.workbook import Workbook
from openpyxl.styles import Alignment
from django.http import HttpResponse
from rest_framework import viewsets
from datetime import datetime
from io import BytesIO
import pandas as pd
import platform
import string
import random
import os


# class ApplicationFormFilterAPIView(viewsets.GenericViewSet):
# class ApplicationFormFilterAPIView(generics.ListAPIView):
class ApplicationFormFilterAPIView(viewsets.ReadOnlyModelViewSet):
    queryset = ApplicationForm.objects.all()
    serializer_class = ApplicationFormFilterSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ApplicationFormFilter

    def get_filtered_data_size(self, queryset):
        df = pd.DataFrame.from_records(queryset.values('start_date', 'finish_date'))
        excel_file = BytesIO()
        df['start_date'] = pd.to_datetime(df['start_date']).dt.tz_localize(None)
        df['finish_date'] = pd.to_datetime(df['finish_date']).dt.tz_localize(None)
        df.to_excel(excel_file, index=False, na_rep="нет значения")
        return excel_file.tell()

    def list(self, request, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        filtered_data_size = self.get_filtered_data_size(queryset)
        count = queryset.count()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'count': count, 'results': serializer.data, 'filtered_data_size': filtered_data_size})


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

        # Создание DataFrame из данных
        df = pd.DataFrame(data)

        # Удаление пустых списков
        df = df.applymap(lambda x: None if x == [] else x)

        # Преобразование значений словарей в строки без скобок и кавычек
        df['status_info'] = df['status_info'].apply(lambda x: ', '.join([f"{item['status']} - {item['date_status']}" for item in x]))
        df['priority_info'] = df['priority_info'].apply(lambda x: ', '.join([f"{item['priority']} - {item['date_priority']}" for item in x]))

        # Создание DataFrame с данными о количестве заявок
        count_df = pd.DataFrame([{'Количество заявок': len(data)}])

        # Объединение основного DataFrame и DataFrame с количеством заявок
        final_df = pd.concat([df, count_df], axis=1)

        # Генерация имени файла
        date_str = datetime.now().strftime('%Y-%m-%d')
        random_suffix = self.generate_random_string()
        filename = f"siroco_{date_str}_report_{random_suffix}.xlsx"
        desktop_path = self.get_desktop_path()
        excel_file_path = os.path.join(desktop_path, filename)

        # Запись данных в Excel с использованием openpyxl
        wb = Workbook()
        ws = wb.active
        ws.append(final_df.columns.tolist())  # Запись заголовков
        for row in dataframe_to_rows(final_df, index=False, header=False):
            ws.append(row)

        # Выравнивание ячеек по левому краю
        for col in ws.columns:
            max_length = 0
            column = col[0].column_letter
            for cell in col:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(cell.value)
                except:
                    pass
            adjusted_width = (max_length + 2)
            ws.column_dimensions[column].width = adjusted_width
            for cell in col:
                cell.alignment = Alignment(horizontal='left', vertical='top', wrap_text=True)

        wb.save(excel_file_path)

        file_size = os.path.getsize(excel_file_path)

        if os.path.exists(excel_file_path):
            os.startfile(excel_file_path)
            return HttpResponse(f"Файл успешно скачан и открыт. Размер файла в байтах: {file_size} байт")
        else:
            return HttpResponse("Не удалось открыть файл")
