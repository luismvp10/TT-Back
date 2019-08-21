from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from users.models import User
from rest_framework.response import Response
from users.permissions import IsAllowedToWrite


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@permission_classes((IsAllowedToWrite,))
def register(request):
    email = request.data.get("email")
    password = request.data.get("password")
    names = request.data.get("names")
    surname = request.data.get("surname")
    if email is None or password is None:
        return Response({'error': 'Please provide both email and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = User.objects.create_user(email, names, surname, password)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@permission_classes((IsAllowedToWrite,))
def delete(request):
    try:
        email = request.data.get("email")
        user = User.objects.get(email=email)
        user.delete()
        return Response({'correct': 'Deleted successfully'},
                        status=HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': 'The user does not exist'},
                        status=HTTP_404_NOT_FOUND)
