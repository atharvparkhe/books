from rest_framework import serializers
from .models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = ["category_name"]


class QuestionSerializer(serializers.ModelSerializer):
    quest_id = serializers.CharField(required = False, read_only=True)
    class Meta:
        model = QuestionModel
        exclude = ["created_at", "updated_at", "user"]


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswersModel
        exclude = ["created_at", "updated_at", "user", "question"]


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookModel
        exclude = ["created_at", "updated_at", "current_owner"]


class PointsTransferSerializer(serializers.Serializer):
    recieptant_email = serializers.EmailField(required = True)
    no_of_points = serializers.IntegerField(required = True)


class otpSerializer(serializers.Serializer):
    otp = serializers.IntegerField(required = True)


class BuySellSerializer(serializers.Serializer):
    book_id = serializers.CharField(required = True)
    seller_email = serializers.EmailField(required = True)