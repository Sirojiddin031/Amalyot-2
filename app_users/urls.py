# urls.py
from django.urls import path, include
from .views import RegisterAPIView, VerifyOTPAPIView, ProfileAPIView, PhoneAPIView, LoginAPIView, UserViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter() # type: ignore
router.register(r'users', UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('send-otp/', PhoneAPIView.as_view(), name='send-otp'),
    path('verify-otp/', VerifyOTPAPIView.as_view(), name='verify-otp'),
    path('me/', ProfileAPIView.as_view(), name='user_profile'),
    path('users/login/', LoginAPIView.as_view(), name='login'),

]


