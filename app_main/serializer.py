from app_main.models import *
from rest_framework import fields, serializers
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
    fileext = serializers.SerializerMethodField()
    class Meta:
        model = BookModel

        fields = "__all__" 

    def get_fileext(self, obj):
        return str(obj.file).split('.')[-1]
    

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


        fields = ['id', 'email', 'name',  'phone','points']


class UpvoteDownVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voting

        fields = "__all__"
