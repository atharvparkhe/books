from rest_framework import serializers


class loginSerializer(serializers.Serializer):
    email = serializers.EmailField(required = True)
    password = serializers.CharField(required = True)


class signupSerializer(serializers.Serializer):
    name = serializers.CharField(required = True)
    email = serializers.EmailField(required = True)
    password = serializers.CharField(required = True)


class otpSerializer(serializers.Serializer):
    otp = serializers.IntegerField(required = True)
    npw = serializers.CharField(required = True)
    cpw = serializers.CharField(required = True)


class emailSerializer(serializers.Serializer):
    email = serializers.EmailField(required = True)