from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializer import *


@api_view(["GET"])
def category(request):
    try:
        cat_objs = CategoryModel.objects.all()
        serializer = CategorySerializer(cat_objs, many=True)
        payload = {"data", serializer.data}
        return Response(payload, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error":e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)