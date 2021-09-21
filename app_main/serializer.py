from app_main.models import *
from rest_framework import serializers
from app_accounts.models import *


class BookSerializer(serializers.ModelSerializer):
    imgs = serializers.ImageField(allow_empty_file=True, required=False)
    
    
    class Meta:
        model = BookModel

        fields = "__all__"

        
class BookPurchasedSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookPurchasedModel

        fields = "__all__"        


class BookViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookModel

        fields = "__all__"        

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionModel

        fields = "__all__"





class AnswerSerializer(serializers.ModelSerializer):

    
    class Meta:
        model = AnswersModel

        fields = "__all__"        


class  CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel

        fields = "__all__"        


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerModel

        exclude = ('password', )