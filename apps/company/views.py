from rest_framework import generics, status, filters
from ..application.views import CustomPagination
from rest_framework.response import Response
from ..company.serializers import *
from ..company.models import Company, JobTitle
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from apps.user.permissions import *
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count


class CompanyListAPIView(generics.ListAPIView):
    '''company list'''
    serializer_class = CompanyListSerializer
    pagination_class = CustomPagination
    permission_classes = [IsManagerCanCreateAndEditCompanyOrIsAdminUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'country', 'company_code']

    def get_queryset(self):
        queryset = Company.objects.annotate(
            count_users=Count('company_users', distinct=True),
            count_applications=Count('applications_count', distinct=True)
        )
        return queryset


class CompanyDetailAPIView(generics.RetrieveAPIView):
    '''company detail only view'''
    serializer_class = CompanyDetailSerializer
    permission_classes = [IsManagerCanCreateAndEditCompanyOrIsAdminUser]
    lookup_field = 'id'

    def get_queryset(self):
        queryset = Company.objects.annotate(
            count_users=Count('company_users', distinct=True),
            count_applications=Count('applications_count', distinct=True),
        )
        return queryset



class CompanyCreateAPIView(generics.CreateAPIView):
    '''company create'''
    queryset = Company.objects.all().select_related('main_manager').prefetch_related('managers')
    serializer_class = CompanyCreateSerializer
    # permission_classes = [IsManagerCanCreateAndEditCompanyOrIsAdminUser]


class CompanyRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    '''company redact'''
    queryset = Company.objects.all().select_related('main_manager').prefetch_related('managers')
    serializer_class = CompanyRetrieveUpdateSerializer
    lookup_field = 'id'
    permission_classes = [IsManagerCanCreateAndEditCompanyOrIsAdminUser]


class CompanyOnlyNameListAPIView(generics.ListAPIView):
    '''company list, only with name, for frontend developers'''
    queryset = Company.objects.all()
    serializer_class = CompanyOnlyNameListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


'''Job Title'''


class JobTitleListAPIView(generics.ListAPIView):
    queryset = JobTitle.objects.all()
    serializer_class = JobTitleSerializer
    permission_classes = [IsManagerCanCreateAndDeleteJobTitleOrIsAdminUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']


class JobTitleDestroyAPIView(generics.DestroyAPIView):
    queryset = JobTitle.objects.all()
    serializer_class = JobTitleSerializer
    permission_classes = [IsManagerCanCreateAndDeleteJobTitleOrIsAdminUser]
    lookup_field = 'id'


class JobTitleCreateAPIView(generics.CreateAPIView):
    queryset = JobTitle.objects.all()
    serializer_class = JobTitleSerializer
    permission_classes = [IsManagerCanCreateAndDeleteJobTitleOrIsAdminUser]


@csrf_exempt
def generate_codes_view(request):
    if request.method == 'GET':
        company_name = request.GET.get('company_name')
        company = Company()
        codes = company.generate_codes(company_name)
        return JsonResponse({'codes': codes}, safe=False)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


class LogoAPIView(APIView):
    def get(self, request):
        logo_path = 'back_static/logo.svg'
        try:
            with open(logo_path, 'rb') as file:
                response = HttpResponse(file.read(), content_type='image/svg+xml')
                return response
        except FileNotFoundError:
            return Response(status=status.HTTP_404_NOT_FOUND)
