from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializer import *
from rest_framework import viewsets
from rest_framework import generics
from app_base.utils import *
from django.core.paginator import Paginator


class BookAdminViewSet(viewsets.ModelViewSet):
    """
    Book CRUD operations
    This Api enables the user to create, retrieve, update and delete books
    """
    
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
        

    queryset = BookModel.objects.all()
    serializer_class = BookSerializer


    def list(self , request):
        objs = self.queryset.filter(current_owner = request.user)
        page = request.GET.get('page', 1)

        paginator = Paginator(objs, 2)
        data = paginate(objs ,paginator , page )

        serializer = self.serializer_class(data['results'] , many = True)
        #print(serializer.data)
        data['results'] = serializer.data

        return Response({
            'status' : 200,
       
            'data' : data 
        })

        

    def create(self, request, *args, **kwargs):
        data = request.data
        data['current_owner'] = request.user
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=200, headers=headers)



class BookBuy(APIView):

    """
    This Api enables the user to buy books
    """
    
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)


    def post(self, request):
        try:
            data = request.data
            book = BookModel.objects.get(id = data['book_id'])
            obj = CustomerModel.objects.get(id = request.user.id)
            if book.credit > obj.points :
                return Response({'message':'Not enough points'}, status=400)

            
            obj.points -= book.credit
            print(obj.points)
            obj.save()     
          
            book.current_owner.points += book.credit
           
            book.current_owner.save()         
            
      
        
            c = BookPurchasedModel.objects.create(user = obj, book = book)
            c.save()
            
            return Response(status=200, data={"message": "Success"})
        except Exception as e:
            print(e)
        return Response(status=400, data={'error':'book not found'})



  
    def get(self,request):
          
        objs = BookPurchasedModel.objects.filter(user = request.user)
        page = request.GET.get('page', 1)

        paginator = Paginator(objs, 2)
        data = paginate(objs ,paginator , page )

        serializer = BookPurchasedSerializer(data['results'] , many = True)
        #print(serializer.data)
        data['results'] = serializer.data

        return Response({
            'status' : 200,
       
            'data' : data 
        })




class AllBooksView(generics.ListAPIView):
    """
    This Api enables the user to view all books
    """
 
    queryset = BookModel.objects.all()
    serializer_class = BookViewSerializer


    def list(self , request):

        if request.GET.get('search'):
            objs = self.queryset.filter(title__icontains = request.GET.get('search'))

        else:
            objs = self.queryset.all()
        page = request.GET.get('page', 1)

        paginator = Paginator(objs, 2)
        data = paginate(objs ,paginator , page )

        serializer = self.serializer_class(data['results'] , many = True)
        #print(serializer.data)
        data['results'] = serializer.data

        return Response({
            'status' : 200,
       
            'data' : data 
        })

        


class QusetionView(generics.ListAPIView):
    """
    This Api enables the user to view all Questions
    """

    queryset = QuestionModel.objects.all()
    serializer_class = QuestionSerializer


    def list(self , request):
        if request.GET.get('search'):
            objs = self.queryset.filter(desc__icontains = request.GET.get('search'))

        else:
            objs = self.queryset.all()
        page = request.GET.get('page', 1)

        paginator = Paginator(objs, 2)
        data = paginate(objs ,paginator , page )

        serializer = self.serializer_class(data['results'] , many = True)
        #print(serializer.data)
        data['results'] = serializer.data

        return Response({
            'status' : 200,
       
            'data' : data 
        })

            


class AnswerView(generics.ListAPIView):
    """
    This Api enables the user to view all Answers specific to a question
    """



    queryset = AnswersModel.objects.all()
    serializer_class = AnswerSerializer




    def list(self , request):
        
        objs = self.queryset.filter(question = self.request.data['question_id'])
        page = request.GET.get('page', 1)

        paginator = Paginator(objs, 2)
        data = paginate(objs ,paginator , page )

        serializer = self.serializer_class(data['results'] , many = True)
        #print(serializer.data)
        data['results'] = serializer.data

        return Response({
            'status' : 200,
       
            'data' : data 
        })

                


class BookPurchasedView(generics.ListAPIView):
    """
    This Api enables the user to view all books purchased
    """

    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = BookPurchasedModel.objects.all()
    serializer_class = BookPurchasedSerializer



    def list(self , request):

        
        
        objs = self.queryset.filter(user = self.request.user)
        page = request.GET.get('page', 1)

        paginator = Paginator(objs, 2)
        data = paginate(objs ,paginator , page )

        serializer = self.serializer_class(data['results'] , many = True)
        #print(serializer.data)
        data['results'] = serializer.data

        return Response({
            'status' : 200,
       
            'data' : data 
        })


class UploadQuestion(viewsets.ModelViewSet):
    """
    This Api enables the user to upload questions
    """
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = QuestionModel.objects.all()
    serializer_class = QuestionSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        data['user'] = request.user
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        obj = CustomerModel.objects.get(id = request.user.id)
        obj.points += 10
        obj.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=200, headers=headers)

   


    def list(self , request):
        objs = self.queryset.filter(user = self.request.user)
        page = request.GET.get('page', 1)

        paginator = Paginator(objs, 2)
        data = paginate(objs ,paginator , page )

        serializer = self.serializer_class(data['results'] , many = True)
        #print(serializer.data)
        data['results'] = serializer.data

        return Response({
            'status' : 200,
       
            'data' : data 
        })





class GetCategory(generics.ListAPIView):
    """
    This Api enables the user to view all categories
    """
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = CategoryModel.objects.all()
    serializer_class = CategorySerializer


class AnswerUpload(generics.CreateAPIView):
    """
    This Api enables the user to answer question
    """

    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = AnswersModel.objects.all()
    serializer_class = AnswerSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        data['user'] = request.user
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        obj = CustomerModel.objects.get(id = request.user.id)
        obj.points += 10
        obj.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=200, headers=headers)


 
class ViewProfile(APIView):
    """
    User Profile details
    """
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)


    def get(self, request):
        try:
            obj = CustomerModel.objects.get(id = request.user.id)
            serializer = CustomerSerializer(obj)
            return Response(serializer.data)
        except Exception as e:
            print(e)
        return Response(status=400, data={'error':'user not found'})

