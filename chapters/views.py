from django.shortcuts import render
from rest_framework import generics
from chapters.models import Chapter
from chapters.serializers import ChapterSerializer
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

# Create your views here.
@permission_classes((AllowAny,))
class ChapterList(generics.ListAPIView):
    queryset = Chapter.objects.all();
    serializer_class = ChapterSerializer
