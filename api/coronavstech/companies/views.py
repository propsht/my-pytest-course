from django.core.mail import send_mail
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.coronavstech.companies.models import Company
from api.coronavstech.companies.serializers import CompanySerializer


class CompanyViewSet(ModelViewSet):
    serializer_class = CompanySerializer
    queryset = Company.objects.all().order_by("-last_update")
    pagination_class = PageNumberPagination


@api_view(http_method_names=["POST"])
def send_company_email(request:Request) -> Response:
    """
    send email with request payload
    sender: propsht.ufo@gmail.com
    receiver: propsht.ufo@gmail.com
    """
    send_mail(
        subject=request.data.get("subject"),
        message=request.data.get("message"),
        from_email="johndoeson303@gmail.com",
        recipient_list=["propsht.ufo@gmail.com"],
    )
    return Response(
        {
            "status": "success",
            "info": "email send successfully"}, status=200
    )
