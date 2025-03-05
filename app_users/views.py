# views.py
from asyncio import timeout
from random import randint
from datetime import date

from django.core.cache import cache
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from yaml import serialize
# import requests
from .models import User
from .serializers import VerifyOTPSerializer, RegisterSerializer, PhoneSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer
import random
from django.core.mail import send_mail
from rest_framework import viewsets, status
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from .models import TokenModel
from .serializers import UserSerializer, OTPSerializer


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'])
    def send_otp(self, request):
        phone = request.data.get("phone")
        otp = request.data.get("otp")

        if not phone or not otp:
            return Response({"error": "Phone and OTP are required"}, status=status.HTTP_400_BAD_REQUEST)

        today_date = date.today()  

        token_obj = TokenModel.objects.create(date=today_date, token=otp)
        return Response({"message": "OTP sent successfully"}, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data["phone"]
            user = User.objects.get(phone=phone)
            
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "is_admin": user.is_admin,
                "is_user": user.is_user,
                "is_staff": user.is_staff,
            })

        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

# url = "http://127.0.0.1:8000/api/v1/users/login/"
# data = {
#     "phone": "+998901234567",
#     "password": "yourpassword"
# }

# response = requests.post(url, json=data)

# if response.status_code == 200:
#     print(response.json())  # JWT token va foydalanuvchi ma'lumotlari
# else:
#     print("Login muvaffaqiyatsiz:", response.json())


class PhoneAPIView(APIView):
    @swagger_auto_schema(request_body=PhoneSerializer)
    def post(self, request):
        serializer = PhoneSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone']

            otp_code = str(randint(1000, 9999))
            print("Yaratilgan OTP:", otp_code)

            cache.set(phone, {"otp": otp_code, "phone_number": phone}, timeout=900)

            return Response(
                {"success":True,"detail":"Sizga kod yuborildi!"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPAPIView(APIView):
        @swagger_auto_schema(request_body=VerifyOTPSerializer)
        def post(self, request):
            serializer = VerifyOTPSerializer(data=request.data)
            if serializer.is_valid():
                phone = serializer.validated_data['phone']
                verification_code = serializer.validated_data['verification_code']
                cached_otp = cache.get(phone)

                if str(cached_otp.get("otp")) == str(verification_code):

                    return Response(
                        {"success":True,"detail":"OTP tasdiqlandi. Endi ro'yxatdan o'tishingiz mumkin."},
                        status=status.HTTP_200_OK
                    )

                return Response(
                    {"success":False,"detail":"Noto‘g‘ri raqam yoki eskirgan OTP kod."},
                     status=status.HTTP_400_BAD_REQUEST
                )

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterAPIView(APIView):
    @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():

            phone = serializer.validated_data['phone']
            cached_data = cache.get(phone)

            if not cached_data:
                return Response(
                    {"success": False, "detail": "Telefon raqamingiz tasdiqlangan raqamga mos emas!"}
                )

            phone_number = cached_data.get("phone_number")

            if str(phone_number) == str(phone):
                serializer.save()
                return Response(
                    {"success": True, "detail": "Ro'yxatdan o'tish muvaffaqiyatli amalga oshirildi!"},
                    status=status.HTTP_201_CREATED
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = RegisterSerializer(request.user)

        return Response(
            {"success":True,"data":serializer.data},
            status=status.HTTP_200_OK
        )

    def patch(self, request):
        serializer = RegisterSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"success":True,"data":serializer.data},
                status=status.HTTP_201_CREATEDOK
            )