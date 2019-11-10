import datetime

from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
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
from users.serializers import UserSerializer


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
        return Response({'error': 'El correo o contraseña son incorrectos'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key,
                     'userType': user.user_type,
                     'name': user.names + ' ' + user.surname},
                    status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@permission_classes((IsAllowedToWrite,))
def register(request):
    email = request.data.get("email")
    password = request.data.get("password")
    names = request.data.get("names")
    surname = request.data.get("surname")
    print(email + " " + password + " " + names + " " + surname)
    if email is None or password is None:
        return Response({'error': 'Please provide both email and password'},
                        status=HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(email=email)
        return Response({'error': 'El correo ingresado ya tiene un usuario asociado'},
                        status=HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
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
        print(email)
        user = User.objects.get(email=email)
        user.delete()
        return Response({'status': True},
                        status=HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'status': False},
                        status=HTTP_404_NOT_FOUND)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def validateToken(request):
    try:
        token = request.data.get("token")
        t = Token.objects.get(key=token)
        return Response({'error': True},
                        status=HTTP_200_OK)
    except Token.DoesNotExist:
        return Response({'error': False},
                        status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def modify(request):
    email = request.data.get("email")
    password = request.data.get("password")
    names = request.data.get("names")
    surname = request.data.get("surname")
    if email is None or password is None:
        return Response({'error': 'Please provide both email and password'},
                        status=HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(email=email)
        user.set_password(password)
        user.names = names
        user.surname = surname
        user.save()
        return Response({'success': 'Usuario modificado correctamente'},
                        status=HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': 'El usuario no existe'},
                        status=HTTP_400_BAD_REQUEST)


@permission_classes((IsAllowedToWrite,))
class UserList(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        token = self.request.auth
        t = Token.objects.filter(key=token).values('user__email')
        return User.objects.exclude(email=u'' + t[0]['user__email'])


from django.core.mail import send_mail

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def send_email(request):
    email = request.data.get("email")
    a = '#$&*-.0123456789@ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz'
    new = ''
    try:
        user = User.objects.get(email=email)
        user.active = False
        user.save()
        for c in email:
            p_ = a.index(c)
            C = (p_ + 10) % 70
            new = new + a[C]
        send_mail(
            'SICAT: Modificar contraseña',
            'Para modificar su contraseña acceda al siguiente link http://localhost:4200/recover/' + new,
            'apikey',
            [email],
            fail_silently=False,
        )
        return Response({'success': 'Se ha enviado un correo a su cuenta para modificar su contraseña'},
                        status=HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': 'No hay una cuenta asociada al correo ingresado'},
                        status=HTTP_400_BAD_REQUEST)
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def recover_password(request):
    email = request.data.get("email")
    password = request.data.get("password")
    if email is None or password is None:
        return Response({'error': 'Please provide both email and password'},
                        status=HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(email=email)
        if user.is_active is True:
            return Response({'error': 'No se solicitó recuperación'},
                            status=HTTP_400_BAD_REQUEST)
        user.set_password(password)
        user.active = True
        user.save()
        return Response({'success': 'Se ha guardado la nueva contraseña'},
                        status=HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': 'El usuario no existe'},
                        status=HTTP_400_BAD_REQUEST)
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def allow_to_recover(request):
    email = request.data.get("email")
    if email is None:
        return Response({'error': 'Please provide both email and password'},
                        status=HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(email=email)
        if user.is_active is True:
            return Response({'error': 'No se solicitó recuperación'},
                            status=HTTP_400_BAD_REQUEST)
        else:
            return Response({'success': 'Puede modificar su contraseña'},
                            status=HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': 'El usuario no existe'},
                        status=HTTP_400_BAD_REQUEST)