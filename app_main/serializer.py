from app_main.models import *
from rest_framework import fields, serializers
from app_accounts.models import *




class BookImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookImage
        fields = ('image',)



class BookSerializer(serializers.ModelSerializer):
    images = BookImageSerializer(source='bookimage_set', many=True, read_only=True)
    
    
    class Meta:
        model = BookModel

        fields = "__all__"


    



    def create(self, validated_data):
        images_data = self.context.get('view').request.FILES
    
        obj = BookModel.objects.create(**validated_data)
        for image_data in images_data.values():
            BookImage.objects.create(book=obj, image=image_data)
        return obj      

        
class BookPurchasedSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookPurchasedModel

        fields = "__all__"        


class BookViewSerializer(serializers.ModelSerializer):
    fileext = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    class Meta:
        model = BookModel

        fields = "__all__" 

    def get_fileext(self, obj):
        return str(obj.file).split('.')[-1]

    def get_images(self, obj):
        return BookImageSerializer(obj.book_image.all(), many=True).data
    

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



class QuestionAnswerSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField()
    class Meta:
        model = QuestionModel

        fields = "__all__"


    def get_answers(self, obj):
        answer_data = None

        try:
            answer_obj = AnswersModel.objects.filter(question=obj.id)
            serializer = AnswerSerializer(answer_obj, many=True)
            answer_data = serializer.data
        except Exception as e:
            print(e)
        return answer_data


class IDSerializer(serializers.Serializer):
    id = serializers.CharField()