from rest_framework import generics
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from chapters.models import Chapter
from shipments.models import Shipment
from shipments.serializers import ShipmentSerializer
from shipments.forms import ShipmentForm
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny

@csrf_exempt
@api_view(["GET", "POST"])
@permission_classes((AllowAny,))

def AddShipment(request):
    form = ShipmentForm()
    if request.method == 'POST':
        shipment = Shipment(id_shipment=request.POST.get('id_shipment'), name=request.POST.get('name'))
        shipment.save()
        shipment = Shipment.objects.filter(id_shipment=request.POST.get('id_shipment')).update(chapter=request.POST.get('id_chapter'))
    elif request.method == 'GET':
        print(request.GET)
    return render(request, 'shipments/AddShipment.html', {"form":form})




# Create your views here.
@permission_classes((AllowAny,))
class ShipmentList(generics.ListAPIView):
    serializer_class = ShipmentSerializer

    def get_queryset(self):
        id = self.kwargs['pk']
        return Shipment.objects.filter(chapter_id=id)
