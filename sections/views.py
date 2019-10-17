from django.shortcuts import render
from rest_framework import generics
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
from sections.forms import SectionForm
from sections.models import Section
from sections.serializers import SectionSerializer


@csrf_exempt
@api_view(["GET", "POST"])
@permission_classes((AllowAny,))

def AddSection(request):
    form = SectionForm()
    if request.method == 'POST':
        section = Section(id_section=request.POST.get('id_section'), name=request.POST.get('name'))
        section.save()
        section = Section.objects.filter(id_section=request.POST.get('id_section')).update(subShipment=request.POST.get('id_subShipment'), id_unity=request.POST.get('unidad'))
    elif request.method == 'GET':
        print(request.GET)
    return render(request, 'sections/AddSection.html', {"form": form})


@permission_classes((AllowAny,))
class SectionList(generics.ListAPIView):
    serializer_class = SectionSerializer

    def get_queryset(self):
        id = self.kwargs['pk']
        return Section.objects.filter(subShipment_id=id)
