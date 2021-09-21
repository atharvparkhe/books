from functools import partial
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


class Question(APIView):
    def get(self, request):
        try:
            ques_objs = QuestionModel.objects.all()
            serializer = QuestionSerializer(ques_objs, many=True)
            return Response({"data":serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            data = request.data
            serializer = QuestionSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"data":serializer.data, "message":"Question added"}, status=status.HTTP_201_CREATED)
            return Response({"errors":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error":e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def patch(self, request):
        try:
            data = request.data
            serializer = QuestionSerializer(data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"data":serializer.data, "message":"Question edited"}, status=status.HTTP_202_ACCEPTED)
            return Response({"errors":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error":e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class Answer(APIView):
    def get(self, request, quest_id):
        try:
            quest_obj = QuestionModel.objects.get(id=quest_id)
            ans_objs = AnswersModel.objects.filter(question=quest_obj)
            serializer = QuestionSerializer(ans_objs, many=True)
            return Response({"data":serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            data = request.data
            serializer = AnswerSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"data":serializer.data, "message":"Answer added"}, status=status.HTTP_201_CREATED)
            return Response({"errors":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error":e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def patch(self, request):
        try:
            data = request.data
            serializer = AnswerSerializer(data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"data":serializer.data, "message":"Answer edited"}, status=status.HTTP_202_ACCEPTED)
            return Response({"errors":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error":e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
