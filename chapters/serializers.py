from rest_framework import serializers
from chapters.models import Chapter

class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields=('id_chapter','name')