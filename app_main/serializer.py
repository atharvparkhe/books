from rest_framework import serializers
from .models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = ["category_name"]


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionModel
        fields = "__all__"