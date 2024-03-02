from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from ..company.models import Company, JobTitle
from ..company.serializers import CompanySerializer, JobTitleSerializer
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt



class BaseViewSet(GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin):
    pass

class CompanyAPIView(BaseViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ['name', 'country']  
    filterset_fields = '__all__'

class JobTitleAPIView(BaseViewSet):
    queryset = JobTitle.objects.all()
    serializer_class = JobTitleSerializer


@csrf_exempt
def generate_codes_view(request):
    if request.method == 'GET':
        company_name = request.GET.get('company_name')
        company = Company()
        codes = company.generate_codes(company_name)
        return JsonResponse(codes, safe=False)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)