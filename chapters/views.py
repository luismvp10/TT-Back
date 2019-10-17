from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from chapters.forms import ChapterForm
from chapters.models import Chapter
from chapters.serializers import ChapterSerializer
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny


@csrf_exempt
@api_view(["GET", "POST"])
@permission_classes((AllowAny,))
def AddChapter(request):
    form = ChapterForm()
    if request.method == 'POST':
        chapter = Chapter(id_chapter=request.POST.get('id_chapter'), name=request.POST.get('name'))
        chapter.save()
    elif request.method == 'GET':
        print(request.GET)
    return render(request, 'chapters/AddChapter.html', {"form": form})



# Create your views here.
@permission_classes((AllowAny,))
class ChapterList(generics.ListAPIView):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer



# Create your views here.
@permission_classes((AllowAny,))
class ChapterSerch(generics.ListAPIView):
    serializer_class = ChapterSerializer

    def get_queryset(self):
        name=self.kwargs['search']
        return Chapter.objects.filter(name__contains=name)








