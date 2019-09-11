from django.shortcuts import render
from django.views.generic import TemplateView
from django.core.serializers import serialize
from django.http import HttpResponse
from django.http import JsonResponse
from .models import Disponible, Trafico, Parking
import datetime
import json
from django.core.serializers.json import DjangoJSONEncoder

# Create your views here.


class HomePageView(TemplateView):
	template_name = 'index.html'

def disponible_datasets_tipo(request, tipo):
	now = datetime.datetime.now()
	parking = None
	if(tipo=="todos"):
		parking = Disponible.objects.filter(hora=now.hour, idParkingModelo__idmodelo=1).values('idParkingModelo__idparking','idParkingModelo__idparking__lat', 'idParkingModelo__idparking__lon', 'idParkingModelo__idparking__precioPorHora','estaLibre', 'idParkingModelo')

	elif(tipo=="libres"):
		parking = Disponible.objects.filter(estaLibre=1, hora=now.hour, idParkingModelo__idmodelo=1).values('idParkingModelo__idparking','idParkingModelo__idparking__lat', 'idParkingModelo__idparking__lon', 'idParkingModelo__idparking__precioPorHora','estaLibre', 'idParkingModelo')

	elif(tipo=="libresGratis"):
		parking = Disponible.objects.filter(estaLibre=1, idParkingModelo__idparking__precioPorHora=0, hora=now.hour, idParkingModelo__idmodelo=1).values('idParkingModelo__idparking','idParkingModelo__idparking__lat', 'idParkingModelo__idparking__lon', 'idParkingModelo__idparking__precioPorHora','estaLibre', 'idParkingModelo')

	elif(tipo=="libresPago"):
		parking = Disponible.objects.filter(estaLibre=1, idParkingModelo__idparking__precioPorHora__gt=0, hora=now.hour, idParkingModelo__idmodelo=1).values('idParkingModelo__idparking','idParkingModelo__idparking__lat', 'idParkingModelo__idparking__lon', 'idParkingModelo__idparking__precioPorHora','estaLibre', 'idParkingModelo')

	disponibles = json.dumps(list(parking), cls=DjangoJSONEncoder)

	return HttpResponse(disponibles, content_type='json')


def trafico_datasets(request):
	now = datetime.datetime.now()
	trafico = Trafico.objects.filter(hora=now.hour, idModeloCalle__idmodelo=1).values('idModeloCalle__idcalle__nombre', 'congestion', 'idModeloCalle__idcalle')
	traficos = json.dumps(list(trafico), cls=DjangoJSONEncoder)
	return HttpResponse(traficos, content_type='json')


def trafico_modelo(request, modelo):
	now = datetime.datetime.now()
	trafico = Trafico.objects.filter(hora=now.hour, idModeloCalle__idmodelo=modelo).values('idModeloCalle__idcalle__nombre', 'congestion', 'idModeloCalle__idcalle')
	traficos = json.dumps(list(trafico), cls=DjangoJSONEncoder)
	return HttpResponse(traficos, content_type='json')


def update_disponible(request):
	
	if request.method == 'POST':
		
		idPark = request.POST['idParkingModelo']
		horaAct = request.POST['hora']
	
		print(idPark,horaAct)

		#print(Disponible.objects.get(idParkingModelo=idPark, hora=horaAct))

		obj = Disponible.objects.get(idParkingModelo=idPark, hora=horaAct)

		#print(obj)

		obj.estaLibre = 0
		obj.save()
		obj.refresh_from_db()

		return JsonResponse({'result':'ok'})

	else:

		return JsonResponse({'result':'nok'})
