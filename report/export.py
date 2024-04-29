from report.serializers import ApplicationFormFilterSerializer
from django_filters.rest_framework import DjangoFilterBackend
from openpyxl.utils.dataframe import dataframe_to_rows
from apps.application.models import ApplicationForm
from report.filters import ApplicationFormFilter
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from openpyxl.workbook import Workbook
from django.utils.http import unquote
from openpyxl.styles import Alignment
from django.http import HttpResponse
from rest_framework import viewsets
from django.conf import settings
from datetime import datetime
from io import BytesIO
import pandas as pd
import threading
import platform
from rest_framework import status
import string
import random
import time
import os
from apps.company.models import Company
from apps.user.permissions import *

class ApplicationFormFilterAPIView(viewsets.GenericViewSet):
    # class ApplicationFormFilterAPIView(generics.ListAPIView):
    # class ApplicationFormFilterAPIView(viewsets.ReadOnlyModelViewSet):
    queryset = ApplicationForm.objects.all()
    serializer_class = ApplicationFormFilterSerializer
    permission_classes = [IsManagerAndClientCanGetReportsOrIsAdminUser]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ApplicationFormFilter

    def get_filtered_data_size(self, queryset):
        df = pd.DataFrame.from_records(queryset.values('start_date', 'finish_date'))
        excel_file = BytesIO()
        # df['start_date'] = pd.to_datetime(df['start_date']).dt.tz_localize(None)
        # df['finish_date'] = pd.to_datetime(df['finish_date']).dt.tz_localize(None)
        df.to_excel(excel_file, index=False, na_rep="нет значения")
        return excel_file.tell()

    def list(self, request, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        filtered_data_size = self.get_filtered_data_size(queryset)
        count = queryset.count()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'count': count,
                         'results': serializer.data,
                         'filtered_data_size': filtered_data_size})


class ExportToExcelView(APIView):
    permission_classes = [IsManagerAndClientCanGetReportsOrIsAdminUser]

    def generate_random_string(self, length=6):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))

    def get(self, request, *args, **kwargs):
        queryset = ApplicationForm.objects.all()
        queryset = ApplicationFormFilter(request.GET, queryset=queryset).qs
        serializer = ApplicationFormFilterSerializer(queryset, many=True)
        data = serializer.data

        df = pd.DataFrame(data)
        for column in df.columns:
            df[column] = df[column].map(lambda x: None if x == [] else x)

        df['status_info'] = df['status_info'].apply(
            lambda x: ',\n '.join([f"{item['status']} - {item['date_status']}" for item in x]) if x else '')

        df['priority_info'] = df['priority_info'].apply(
            lambda x: ',\n '.join([f"{item['priority']} - {item['date_priority']}" for item in x]) if x else '')

        count_df = pd.DataFrame([{'Количество заявок': len(data)}])

        final_df = pd.concat([df, count_df], axis=1)

        date_str = datetime.now().strftime('%Y-%m-%d')
        random_suffix = self.generate_random_string()
        filename = f"siroco_{date_str}_report_{random_suffix}.xlsx"

        wb = Workbook()
        ws = wb.active
        ws.append(final_df.columns.tolist())
        for row in dataframe_to_rows(final_df, index=False, header=False):
            ws.append(row)

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

        excel_file = BytesIO()
        wb.save(excel_file)

        response = HttpResponse(excel_file.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename={unquote(filename)}'
        response['Content-Transfer-Encoding'] = 'binary'
        response['Expires'] = '0'
        response['Cache-Control'] = 'must-revalidate'
        response['Pragma'] = 'public'

        return response
