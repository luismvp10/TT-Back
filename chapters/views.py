from django.shortcuts import render
from rest_framework import generics
from chapters.models import Chapter
from chapters.serializers import ChapterSerializer

class ChapterList(generics.ListAPIView):
    queryset = Chapter.objects.all();
    serializer_class = ChapterSerializer
