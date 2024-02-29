from apps.application.serializers import ApplicationFormSerializer
from django_filters.rest_framework import DjangoFilterBackend
from apps.application.models import ApplicationForm
from rest_framework.viewsets import GenericViewSet
from rest_framework.filters import SearchFilter
from rest_framework import mixins


class BaseViewSet(GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin):
    pass


class ApplicationFormAPIView(BaseViewSet):
    queryset = ApplicationForm.objects.all()
    serializer_class = ApplicationFormSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = '__all__'
    filterset_fields = ['task_number', 'title', 'description', 'username', 'manager', 'start_date', 'priority',
                        'status']


# class ApplicationFormFilterAPIView(viewsets.GenericViewSet):
#     queryset = ApplicationForm.objects.all()
#     serializer_class = ApplicationFormSerializer
#     filter_backends = [DjangoFilterBackend, SearchFilter]
#     # search_fields = ['company__name', 'manager__first_name']
#     filterset_class = ApplicationFormFilter
#
#     def list(self, request, **kwargs):
#         queryset = self.filter_queryset(self.get_queryset())
#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data)
#
#
# class ExportToExcelView(APIView):
#     def get_desktop_path(self):
#         system = platform.system()
#         if system == 'Windows':
#             desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Documents')
#         elif system == 'Darwin':  # macOS
#             desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
#         elif system == 'Linux':
#             desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
#         else:
#             desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
#         return desktop_path
#
#     def generate_random_string(self, length=6):
#         letters = string.ascii_lowercase
#         return ''.join(random.choice(letters) for i in range(length))
#
#     def get(self, request, *args, **kwargs):
#         queryset = ApplicationForm.objects.all()
#         queryset = ApplicationFormFilter(request.GET, queryset=queryset).qs
#         serializer = ApplicationFormSerializer(queryset, many=True)
#         data = serializer.data
#
#         df = pd.DataFrame(data)
#         date_str = datetime.now().strftime('%Y-%m-%d')
#         random_suffix = self.generate_random_string()
#         filename = f"siroco_{random_suffix}_report_{date_str}.xlsx"
#         desktop_path = self.get_desktop_path()
#         excel_file_path = os.path.join(desktop_path, filename)
#         df.to_excel(excel_file_path, index=False)
#
#         file_size = os.path.getsize(excel_file_path)
#         print(f"Размер файла в байтах: {file_size}")
#
#         if os.path.exists(excel_file_path):
#             os.startfile(excel_file_path)
#             return HttpResponse("Файл успешно скачан и открыт")
#         else:
#             return HttpResponse("Не удалось открыть файл")
