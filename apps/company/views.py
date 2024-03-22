import mimetypes

from rest_framework import generics, status
from rest_framework.response import Response

from ..company.models import Company, JobTitle
from ..company.serializers import CompanySerializer, JobTitleSerializer
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import FileResponse
from rest_framework.views import APIView


class CompanyCreateAPIView(generics.CreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class CompanyRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    lookup_field = 'id'


class CompanyListAPIView(generics.ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class JobTitleListAPIView(generics.ListAPIView):
    queryset = JobTitle.objects.all()
    serializer_class = JobTitleSerializer


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
