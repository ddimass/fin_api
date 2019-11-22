from django.http import HttpResponse, JsonResponse
from .models import Bar, Instrument
from .serializers import BarSerializer, InstrumentSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
import datetime
from django.conf import settings
import numpy as np
from keras.utils import to_categorical
from sklearn import preprocessing


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


@csrf_exempt
@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def api_bars(request):
    if request.method == 'GET':
        bars = Bar.objects.filter(created_by=request.user)
        for filter_field in ('timeframe'):
            if request.GET.get(filter_field):
                bars = bars.filter(**{filter_field: request.GET[filter_field]})
        if (request.GET.get('for_predict')):
            bars = bars.filter()[:30]
        # return HttpResponse(bars[0]);
        serializer = BarSerializer(bars, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        if not isinstance(data['instrument'], int):
            instrument = Instrument.objects.get(name=data['instrument'].upper(), created_by = request.user)
        else:
            instrument = Instrument.objects.get(id=data['instrument'], created_by = request.user)
        time = datetime.datetime.strptime(data['time'], "%Y.%m.%d %H:%M:%S").isoformat().replace('T', ' ')
        print("Time: "+ time)
        data['time'] = time;
        serializer = BarSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save(instrument=instrument, time=time)
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)


def django_to_numpy(models, names):
    '''Convert django model to numpy array'''
    for j, model in enumerate(models):
        a = np.zeros((1,len(names)))
        for i,prop in enumerate(names):
            if isinstance(getattr(model, prop), datetime.datetime):
                a[0,i] = getattr(model, prop).isoweekday()
            else:
                a[0,i] = getattr(model, prop)
        if j == 0:
            b = a
        else:
            b = np.append(b, a, 0)
    return b


@csrf_exempt
@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def api_ai(request):
    if request.method == 'GET':
        bars = Bar.objects.filter(created_by=request.user, timeframe='16386')[:50]
        if (len(bars) > 0):
            X = django_to_numpy(bars, ['time', 'open', 'high', 'low', 'close', 'tick_volume'])
        else:
            print('No enouth Bars from DB')
        bin_days = to_categorical(X[:, 0], num_classes=8)
        X = np.delete(X, 0, 1)
        X = np.concatenate((bin_days, X), axis=1)
        X = preprocessing.MinMaxScaler().fit_transform(X)
        X = X.reshape(1,50,13)
        print(X[0][0])
        model = settings.MOD
        y = model.predict(X)
        print(y)
        serializer = BarSerializer(bars, many=True)
        return Response(serializer.data)


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

