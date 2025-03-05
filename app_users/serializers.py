from random import randint
from rest_framework import serializers

from .models import User
from django.contrib.auth import get_user_model
from .models import TokenModel


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone', 'full_name', 'is_active']


class OTPSerializer(serializers.Serializer):
    phone = serializers.CharField()
    code = serializers.CharField()


class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone',)


class RegisterSerializer(serializers.ModelSerializer):

    confirm_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ("id","is_user","is_admin","full_name","phone","password","confirm_password")

    def validate(self, data):
        password = data.get("password")
        confirm_password = data.get("confirm_password")

        if password != confirm_password:
            raise serializers.ValidationError("Passwords must match")

        return data


    def create(self, validated_data):
        """ Yangi foydalanuvchini yaratish """
        password = validated_data.get("password")
        validated_data.pop("confirm_password")

        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.is_active = True
        user.save()
        return user


class VerifyOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15)
    verification_code = serializers.CharField(max_length=4)


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        phone = data.get("phone")
        password = data.get("password")

        user = User.objects.filter(phone=phone).first()
        if not user or not user.check_password(password):
            raise serializers.ValidationError("Phone yoki parol noto‘g‘ri")

        return data


