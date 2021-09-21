from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from .serializer import *
from .threads import *
from .models import *


@api_view(["GET"])
def category(request):
    try:
        cat_objs = CategoryModel.objects.all()
        serializer = CategorySerializer(cat_objs, many=True)
        return Response({"data":serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Question(APIView):
    def get(self, request):
        try:
            ques_objs = QuestionModel.objects.all()
            serializer = QuestionSerializer(ques_objs, many=True)
            return Response({"data":serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            data = request.data
            user_obj = CustomerModel.objects.get(email=request.user.email)
            serializer = QuestionSerializer(data=data)
            if serializer.is_valid():
                serializer.save(user=user_obj)
                return Response({"data":serializer.data, "message":"Question added"}, status=status.HTTP_201_CREATED)
            return Response({"errors":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def patch(self, request):
        try:
            data = request.data
            user_obj = CustomerModel.objects.get(email=request.user.email)
            quest_obj = QuestionModel.objects.get(id=data["quest_id"])
            serializer = QuestionSerializer(quest_obj, data=data, partial=True)
            if serializer.is_valid():
                serializer.save(user=user_obj)
                return Response({"data":serializer.data, "message":"Question edited"}, status=status.HTTP_202_ACCEPTED)
            return Response({"errors":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class Answer(APIView):
    def get(self, request):
        try:
            data=request.data
            quest_obj = QuestionModel.objects.get(id=data["quest_id"])
            ans_objs = AnswersModel.objects.filter(question=quest_obj)
            serializer = AnswerSerializer(ans_objs, many=True)
            return Response({"data":serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            data = request.data
            user_obj = CustomerModel.objects.get(email=request.user.email)
            quest_obj = QuestionModel.objects.get(id=data["quest_id"])
            serializer = AnswerSerializer(data=data)
            if serializer.is_valid():
                serializer.save(question=quest_obj, user=user_obj)
                return Response({"data":serializer.data, "message":"Answer added"}, status=status.HTTP_201_CREATED)
            return Response({"errors":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def patch(self, request):
        try:
            data = request.data
            quest_obj = QuestionModel.objects.get(id=data["quest_id"])
            user_obj = CustomerModel.objects.get(email=request.user.email)
            serializer = AnswerSerializer(data=data, partial=True)
            if serializer.is_valid():
                serializer.save(question=quest_obj, user=user_obj)
                return Response({"data":serializer.data, "message":"Answer edited"}, status=status.HTTP_202_ACCEPTED)
            return Response({"errors":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Book(APIView):
    def get(self, request):
        try:
            book_objs = BookModel.objects.filter(for_sale=False)
            serializer = BookSerializer(book_objs, many=True)
            return Response({"data":serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            data = request.data
            user_obj = CustomerModel.objects.get(email=request.user.email)
            serializer = BookSerializer(data=data)
            if serializer.is_valid():
                serializer.save(current_owner=user_obj)
                return Response({"data":serializer.data, "message":"Book added"}, status=status.HTTP_201_CREATED)
            return Response({"errors":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def patch(self, request):
        try:
            data = request.data
            book_obj = BookModel.objects.get(id=data["book_id"])
            user_obj = CustomerModel.objects.get(email=request.user.email)
            serializer = BookSerializer(book_obj, data=data, partial=True)
            if serializer.is_valid():
                serializer.save(current_owner=user_obj)
                return Response({"data":serializer.data, "message":"Book details edited"}, status=status.HTTP_202_ACCEPTED)
            return Response({"errors":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def gift_points(request):
    try:
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]
        data = request.data
        serializer = PointsTransferSerializer(data=data)
        if serializer.is_valid():
            user_obj = CustomerModel.objects.get(email=request.user.email)
            recieptant = CustomerModel.objects.get(email=serializer.data["recieptant_email"])
            no_of_points = int(serializer.data["no_of_points"])
            serializer = PointsTransferSerializer(data=data)
            with transaction.atomic():
                if not recieptant:
                    return Response({"data":serializer.data, "message":"User does not exist"}, status=status.HTTP_406_NOT_ACCEPTABLE)
                if user_obj.points > no_of_points:
                    user_obj.points -= no_of_points
                    recieptant.points += no_of_points
                    thread_obj = send_transaction_email(recieptant.email, user_obj.name, no_of_points)
                    thread_obj.start()
                    user_obj.save()
                    recieptant.save()
                    return Response({"data":serializer.data, "message":"Points transfered successfully"}, status=status.HTTP_200_OK)
                return Response({"data":serializer.data, "message":"Insufficient point"}, status=status.HTTP_409_CONFLICT)
        return Response({"errors":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def request_points(request):
    try:
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]
        data = request.data
        serializer = PointsTransferSerializer(data=data)
        if serializer.is_valid():
            user_obj = CustomerModel.objects.get(email=request.user.email)
            recieptant = CustomerModel.objects.get(email=serializer.data["recieptant_email"])
            if not recieptant:
                return Response({"message":"User does not exist"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            no_of_points = int(serializer.data["no_of_points"])
            thread_obj = send_request_email(recieptant.email, user_obj.name, no_of_points)
            thread_obj.start()
            return Response({"data":serializer.data, "message":"Request email sent"}, status=status.HTTP_200_OK)
        return Response({"errors":serializer.errors}, status=status.HTTP_406_NOT_ACCEPTABLE)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def buy(request):
    try:
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]
        data = request.data
        serializer = BuySellSerializer(data=data)
        if serializer.is_valid():
            book_obj = BookModel.objects.get(id=serializer.data["book_id"])
            if book_obj.for_sale == True:
                buyer = CustomerModel.objects.get(email=request.user.email)
                seller = CustomerModel.objects.get(email=data["seller_email"])
                thread_obj = buy_request_email(buyer, seller.email, book_obj.title)
                thread_obj.start()
                return Response({"message":"Buy request email sent"}, status=status.HTTP_200_OK)
            return Response({"message":"This book is no longer for sell"}, status=status.HTTP_409_CONFLICT)
        return Response({"errors":serializer.errors}, status=status.HTTP_406_NOT_ACCEPTABLE)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def sell(request):
    try:
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]
        data = request.data
        serializer = BuySellSerializer(data=data)
        if serializer.is_valid():
            book_obj = BookModel.objects.get(id=serializer.data["book_id"])
            if book_obj.for_sale == True:
                buyer = CustomerModel.objects.get(email=request.user.email)
                seller = CustomerModel.objects.get(email=serializer.data["seller_email"])
                with transaction.atomic():
                    if buyer.points > book_obj.value:
                        buyer.points -= book_obj.value
                        seller.points += book_obj.value
                        thread_obj = transaction_email(buyer, seller, book_obj)
                        thread_obj.start()
                        TransactionsModel.objects.create(seller=seller, buyer=buyer, book=book_obj)
                        buyer.save()
                        seller.save()
                    return Response({"message":"Insufficient point"}, status=status.HTTP_409_CONFLICT)
        return Response({"errors":serializer.errors}, status=status.HTTP_406_NOT_ACCEPTABLE)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)