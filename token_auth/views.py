from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Token
from .serializers import UserSerializer
from rest_framework.status import HTTP_403_FORBIDDEN, \
    HTTP_400_BAD_REQUEST
from django.db.utils import IntegrityError


class TokenView(APIView):

    def post(self, request):

        username = request.data.get('username', None)
        password = request.data.get('password', None)

        serializer = UserSerializer(data={
            'username': username,
            'password': password
        })

        if serializer.is_valid():

            user = authenticate(
                username=serializer.initial_data['username'],
                password=serializer.initial_data['password']
            )

            if user is not None:
                return Response({
                    "token": Token.objects.get(user=user).key
                })

            return Response({
                "denied": "wrong username or password"
            }, HTTP_403_FORBIDDEN)

        return Response(serializer.errors,
                        HTTP_400_BAD_REQUEST)


class RegistrationView(APIView):

    def post(self, request):

        username = request.data.get('username', None)
        password = request.data.get('password', None)

        serializer = UserSerializer(data={
            'username': username,
            'password': password
        })

        if serializer.is_valid():

            try:
                User.objects.create_user(
                    username=serializer.initial_data['username'],
                    password=serializer.initial_data['password']
                )
            except IntegrityError:
                return Response({
                    "status": "this username already exists"
                }, HTTP_403_FORBIDDEN)

            return Response({
                "status": "successfully created"
            })

        return Response(serializer.errors,
                        HTTP_400_BAD_REQUEST)
