from django.http import HttpResponse, JsonResponse
from .models import Bar, Instrument
from .serializers import BarSerializer, InstrumentSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication



def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


@csrf_exempt
@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def api_bars(request):
    if request.method == 'GET':
        bars = Bar.objects.filter(created_by=request.user)
        # return HttpResponse(bars[0]);
        serializer = BarSerializer(bars, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        if not isinstance(data['instrument'], int):
            instrument = Instrument.objects.get(name=data['instrument'].upper(), created_by = request.user)
        else:
            instrument = Instrument.objects.get(id=data['instrument'], created_by = request.user)
        serializer = BarSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save(instrument=instrument)
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def api_instruments(request):
    if request.method == 'GET':
        instruments = Instrument.objects.all()
        # return HttpResponse(bars[0]);
        serializer = InstrumentSerializer(instruments, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = InstrumentSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

