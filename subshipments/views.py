from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
from subshipments.forms import SubshipmentForm
from subshipments.models import Subshipment
from subshipments.serializers import SubshipmentSerializer

# Create your views here.
@csrf_exempt
@api_view(["GET", "POST"])
@permission_classes((AllowAny,))
def AddSubshipment(request):
    form = SubshipmentForm()
    if request.method=='POST':
        subshipment = Subshipment(id_subShipment=request.POST.get('id_subShipment'), name=request.POST.get('name'))
        subshipment.save()
        subshipment = Subshipment.objects.filter(id_subShipment=request.POST.get('id_subShipment')).update(shipment=request.POST.get('id_shipment'))
    elif request.method == 'GET':
        print(request.GET)
    return render(request, 'subshipments/AddSubshipment.html', {"form": form})



@permission_classes((AllowAny,))
class SubshipmentList(generics.ListAPIView):
    serializer_class = SubshipmentSerializer

    def get_queryset(self):
        id = self.kwargs['pk']
        return Subshipment.objects.filter(shipment_id=id)

