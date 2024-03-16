from rest_framework import generics, request
from ..company.models import Company, JobTitle
from ..company.serializers import CompanySerializer, JobTitleSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated


class CompanyListAPIView(generics.ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        print(request.user)
        return super().list(request, *args, **kwargs)



class CompanyCreateAPIView(generics.CreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class CompanyRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    lookup_field = 'id'


class JobTitleListCreateAPIView(generics.ListCreateAPIView):
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
