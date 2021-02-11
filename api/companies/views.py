# DRF
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

# Serializers
from .serializers import CompanySerializer

# Models
from .models import Company

from django.core.mail import send_mail


class CompanyViewSet(viewsets.ModelViewSet):
    serializer_class = CompanySerializer
    queryset = Company.objects.all().order_by("-last_update")
    pagination_class = PageNumberPagination

@api_view(http_method_names=["POST"])
def send_company_email(request):
    """
        sends email with request payload
    """
    subject = request.data.get("subject")
    message = request.data.get("message")
    send_mail(
        subject=subject, 
        message=message,
        from_email="luis.e.3194@gmail.com",
        recipient_list=["luis.e.3194@gmail.com"]
    )
    return Response({
        "status": "SUCCESS",
        "info": "Email sent successfully"
    }, status=status.HTTP_200_OK)