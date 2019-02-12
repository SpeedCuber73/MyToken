from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from .models import Token


@api_view(['POST', ])
def get_token(request):
    print("got")
    user = authenticate(
        username=request.data['username'],
        password=request.data['password']
    )
    print("user:", user)
    if user is not None:
        return Response({
            'token': Token.objects.get(user=user).key
        })
    else:
        return Response({
            'credentials': 'Wrong username or password'
        })
