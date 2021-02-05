# DRF
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

# Serializers
from .serializers import CompanySerializer

# Models
from .models import Company


class CompanyViewSet(viewsets.ModelViewSet):
    serializer_class = CompanySerializer
    queryset = Company.objects.all().order_by("-last_update")
    pagination_class = PageNumberPagination
