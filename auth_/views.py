from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from common.utils import unauthorized, ok, bad_request, created
from .messages import invalid_credentials, logout_msg
from .models import User
from .serializers import (
    UserSerializer, RegistrationSerializer, UserLoginSerializer
)
from .utils import get_tokens_for_user


def pong(self):
    return HttpResponse('pong')


class UserList(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    queryset = User.objects.all()


class Registration(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        ser = RegistrationSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return created(ser.data)
        return bad_request(ser.errors)


class UserLogin(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        ser = UserLoginSerializer(data=request.data)
        if ser.is_valid():
            user = ser.data
            user = authenticate(request, username=user['username'], password=user['password'])
            if user is not None:
                login(request, user)
                auth_data = get_tokens_for_user(user)
                return ok(auth_data)
            return unauthorized(invalid_credentials)
        return bad_request(ser.errors)


class UserLogout(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        logout(request)
        return ok(logout_msg)
