from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.core.paginator import Paginator
from app_base.utils import paginate
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
            if request.GET.get('search'):
                ques_objs = QuestionModel.objects.filter(desc__icontains = request.GET.get('search'))
            else:
                ques_objs = QuestionModel.objects.all()
            page_no = request.GET.get('page', 1)
            paginator = Paginator(ques_objs, 5)
            data = paginate(ques_objs, paginator, page_no)
            serializer = QuestionSerializer(data["results"], many=True)
            data["results"] = serializer.data
            return Response({"data":data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def post(self, request):
        try:
            authentication_classes = [JWTAuthentication]
            permission_classes = [IsAuthenticated]
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
            authentication_classes = [JWTAuthentication]
            permission_classes = [IsAuthenticated]
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
    def post(self, request):
        try:
            authentication_classes = [JWTAuthentication]
            permission_classes = [IsAuthenticated]
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
            authentication_classes = [JWTAuthentication]
            permission_classes = [IsAuthenticated]
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
    def post(self, request):
        try:
            authentication_classes = [JWTAuthentication]
            permission_classes = [IsAuthenticated]
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
            authentication_classes = [JWTAuthentication]
            permission_classes = [IsAuthenticated]
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


@api_view(["POST"])
def voting(request):
    try:
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]
        data = request.data
        serializer = VotingSerializer(data=data)
        if serializer.is_valid():
            if not data["quest_id"] and data["ans_id"]:
                return Response({"message":"either of qustion or answer id is needed"}, status=status.HTTP_417_EXPECTATION_FAILED)
            if data["quest_id"]:
                quest_obj = QuestionModel.objects.get(id = data["quest_id"])
                user_obj = CustomerModel.objects.get(email=quest_obj.user.email)
                if data["isUpVote"]:
                    user_obj.points += 5
                    quest_obj.votes += 1
                    user_obj.save()
                    quest_obj.save()
                    return Response({"message":"up vote successfull"}, status=status.HTTP_202_ACCEPTED)
                elif data["isDownVote"]:
                    quest_obj.votes -= 1
                    quest_obj.save()
                    return Response({"message":"down vote successfull"}, status=status.HTTP_202_ACCEPTED)
                else : return Response({"message":"invalid query"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            if data["ans_id"]:
                ans_obj = QuestionModel.objects.get(id = data["ans_id"])
                user_obj = CustomerModel.objects.get(email=ans_obj.user.email)
                if data["isUpVote"]:
                    user_obj.points += 5
                    ans_obj.votes += 1
                    user_obj.save()
                    ans_obj.save()
                    return Response({"message":"up vote successfull"}, status=status.HTTP_202_ACCEPTED)
                elif data["isDownVote"]:
                    ans_obj.votes -= 1
                    ans_obj.save()
                    return Response({"message":"down vote successfull"}, status=status.HTTP_202_ACCEPTED)
                else : return Response({"message":"invalid query"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response({"errors":serializer.errors}, status=status.HTTP_406_NOT_ACCEPTABLE)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)