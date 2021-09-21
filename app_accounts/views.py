from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from app_accounts.models import CustomerModel
from .models import *
from .threads import *
from .serializer import *


@api_view(["POST"])
def signUp(request):
    try:
        data = request.data
        serializer = signupSerializer(data=data)
      
        if serializer.is_valid():
        
            name = serializer.data["name"]
            email = serializer.data["email"]
            password = serializer.data["password"]
            if CustomerModel.objects.filter(email=email).first():
                
                return Response({"status":400, "result":"Acount already exists."})
            else:
               
                new_customer = CustomerModel.objects.create(email=email, name=name)
           
                new_customer.set_password(password)
                thread_obj = send_verification_email(email)
                thread_obj.start()
                new_customer.save()
                return Response({"status":200, "result":"Account created, verification mail sent"})
        return Response({"status":400, "error":serializer.errors})
    except Exception as e:
        print(e)
        return Response({"status":500, "error":e, "message":"Something went wrong"})

@api_view(["POST"])
def verify(request):
    try:
        data = request.data
        serializer = otpSerializer(data=data)
        if serializer.is_valid():
            otp = serializer.data["otp"]
            if not cache.get(otp):
                return Response({"status":400, "result":"OTP expired"})
            user_obj = CustomerModel.objects.filter(email=cache.get(otp)).first()
            if user_obj:
                if user_obj.is_verified:
                    return Response({"status":400, "result":"Account is already verified"})
                user_obj.is_verified = True
                user_obj.save()
                return Response({"status":200, "result":"Account verification successfull"})
    except Exception as e:
        print(e)
    return Response({"status":500, "error":e, "message":"Something went wrong"})

@api_view(["POST"])
def logIn(request):
    try:
        data = request.data
        serializer = loginSerializer(data=data)
        if serializer.is_valid():
            email = serializer.data["email"]
            password = serializer.data["password"]
            customer_obj = CustomerModel.objects.filter(email=email).first()
            if customer_obj is None:
                return Response({"status":400, "result":"Account does not exist"})
            if not customer_obj.is_verified:
                return Response({"status":400, "result":"Email not verified. Check your mail"})
            user = authenticate(email=email, password=password)
            if not user:
                return Response({"status":400, "result":"Incorrect password"})
            jwt_token = RefreshToken.for_user(user)
            return Response({"status":200, "result":"Login successfull", "token":str(jwt_token.access_token)})
        return Response({"status":400, "error":serializer.errors})
    except Exception as e:
        print(e)
        return Response({"status":500, "error":e, "message":"Something went wrong"})

@api_view(["POST"])
def forgot(request):
    try:
        data = request.data
        serializer = emailSerializer(data=data)
        if serializer.is_valid():
            email = serializer.data["email"]
            if not CustomerModel.objects.get(email=email):
                return Response({"status":400, "result":"Account does not exists"})
            thread_obj = send_forgot_link(email)
            thread_obj.start()
            return Response({"status":200, "result":"reset mail sent"})
        return Response({"status":400, "error":serializer.errors})
    except Exception as e:
        print(e)
        return Response({"status":500, "error":e, "message":"Something went wrong"})

@api_view(["POST"])
def reset(request):
    try:
        data = request.data
        serializer = otpSerializer(data=data)
        if serializer.is_valid():
            otp = serializer.data["otp"]
            if not cache.get(otp):
                return Response({"status":400, "result":"OTP expired"})
            if not CustomerModel.objects.filter(email=cache.get(otp)).first():
                return Response({"status":400, "message":"user does not exist"})
            user_obj = CustomerModel.objects.get(email=cache.get(otp))
            npw = serializer.data["npw"]
            cpw = serializer.data["cpw"]
            if npw == cpw:
                user_obj.set_password(cpw)
                user_obj.save()
                return Response({"status":200, "result":"Password changed successfull"})
        else:return Response({"status":400, "error":serializer.errors})
    except Exception as e:
        print(e)
        return Response({"status":500, "error":e, "message":"Something went wrong"})