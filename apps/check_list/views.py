from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from .models import Checklist
from .serializers import ChecklistSerializer

class ChecklistAPIView(GenericViewSet,
                       mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.CreateModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin):
    queryset = Checklist.objects.all()
    serializer_class = ChecklistSerializer
