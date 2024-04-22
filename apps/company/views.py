from rest_framework import generics, status, filters
from ..application.views import CustomPagination
from rest_framework.response import Response
from ..company.models import Company, JobTitle
from ..company.serializers import *
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from apps.user.permissions import *


class CompanyListAPIView(generics.ListAPIView):
    '''company list'''
    queryset = Company.objects.all()
    serializer_class = CompanyListSerializer
    pagination_class = CustomPagination
    # permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']



class CompanyDetailAPIView(generics.RetrieveAPIView):
    '''company detail only view'''
    queryset = Company.objects.all()
    serializer_class = CompanyDetailSerializer
    lookup_field = 'id'
    # permission_classes = [IsAdminUser]


class CompanyCreateAPIView(generics.CreateAPIView):
    '''company create'''
    queryset = Company.objects.all()
    serializer_class = CompanyCreateSerializer
    # permission_classes = [IsAdminUser]


class CompanyRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    '''company redact'''
    queryset = Company.objects.all()
    serializer_class = CompanyRetrieveUpdateSerializer
    lookup_field = 'id'
    # permission_classes = [IsAdminUser]




class JobTitleListAPIView(generics.ListAPIView):
    queryset = JobTitle.objects.all()
    serializer_class = JobTitleSerializer
    # permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']


class JobTitleDestroyAPIView(generics.DestroyAPIView):
    queryset = JobTitle.objects.all()
    serializer_class = JobTitleSerializer
    lookup_field = 'id'


class JobTitleCreateAPIView(generics.CreateAPIView):
    queryset = JobTitle.objects.all()
    serializer_class = JobTitleSerializer



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
