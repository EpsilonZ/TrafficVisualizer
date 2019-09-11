from django.db import models

# Create your models here.

class Modelo(models.Model):
	descripcion = models.CharField(max_length=200)
	

	def __str__(self):
		return "ID: " + str(self.id) + " Descripcion: " + self.descripcion

class Parking(models.Model):
	id = models.DecimalField(max_digits=12, decimal_places=0, default=0, primary_key=True)
	lat = models.FloatField()
	lon = models.FloatField()
	precioPorHora = models.FloatField()
	parkmodelo = models.ManyToManyField(Modelo, through='ParkingModelo', related_name='parkingmodelo')
	

	def __str__(self):
		return "ID: " + str(self.id) + " Lat: " + str(self.lat) + " Lon: " + str(self.lon) + " Precio por hora: " + str(self.precioPorHora)


class Calle(models.Model):
	nombre = models.CharField(max_length=200)
	id = models.DecimalField(max_digits=15, decimal_places=0, default=0, primary_key=True)
	modelocalle = models.ManyToManyField(Modelo, through='ModeloCalle', related_name='callemodelo')
	
	def __str__(self):
		return "ID: " + str(self.id) + " Nombre: " + self.nombre


class ModeloCalle(models.Model):
	idcalle = models.ForeignKey(Calle, to_field='id', on_delete=models.CASCADE, related_name='idcallemodelocalle')
	idmodelo = models.ForeignKey(Modelo, to_field='id', on_delete=models.CASCADE, related_name='idmodelomodelocalle')
	

	class Meta:
		unique_together = (("idcalle", "idmodelo"),)

	def __str__(self):
		return "ID Calle: " + str(self.idcalle.id) + " ID Modelo: " + str(self.idmodelo.id)

class ParkingModelo(models.Model):
	idparking = models.ForeignKey(Parking, to_field='id', on_delete=models.CASCADE, related_name='idparkingparkingmodelo')
	idmodelo = models.ForeignKey(Modelo, to_field='id', on_delete=models.CASCADE, related_name='idmodeloparkingmodelo')
	

	class Meta:
		unique_together = (("idparking", "idmodelo"),)

	def __str__(self):
		return "ID Parking: " + str(self.idparking.id) + " ID Modelo: " + str(self.idmodelo.id)

class Hora(models.Model):
	hora = models.DecimalField(max_digits=8, decimal_places=0, default=0, primary_key=True)
	trafico = models.ManyToManyField(ModeloCalle, through='Trafico', related_name='trafico')
	disponible = models.ManyToManyField(ParkingModelo, through='Disponible', related_name='disponible')
	

	def __str__(self):
		return str(self.hora)

class Trafico(models.Model):

	idModeloCalle = models.ForeignKey(ModeloCalle, to_field='id', on_delete=models.CASCADE, related_name='identificadorcalle')
	hora = models.ForeignKey(Hora, to_field='hora', on_delete=models.CASCADE, related_name='horatrafico')
	congestion = models.DecimalField(max_digits=8, decimal_places=0, default=0)
	

	class Meta:
		unique_together = (("idModeloCalle", "hora"),)


	def __str__(self):
		return "ID: " + str(self.idModeloCalle.idcalle.id) + " Nombre calle: " + str(self.idModeloCalle.idcalle.nombre) \
+ " Hora: "  + str(self.hora) + " Congestion: " + str(self.congestion)

class Disponible(models.Model):

	idParkingModelo = models.ForeignKey(ParkingModelo, to_field='id', on_delete=models.CASCADE, related_name='identificadorparking')
	hora = models.ForeignKey(Hora, to_field='hora', on_delete=models.CASCADE, related_name='horadisponible')
	estaLibre = models.BooleanField()
	


	class Meta:
		unique_together = (("idParkingModelo", "hora"),)

	def __str__(self):
		return str(self.idParkingModelo) + " Hora: " + str(self.hora) + " Esta libre: " + str(self.estaLibre)

