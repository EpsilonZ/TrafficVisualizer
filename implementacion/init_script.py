import psycopg2
from clases.Modelo import Modelo
from clases.Parking import Parking
from clases.Trafico import Trafico
from clases.Hora import Hora
from random import randint
# main starts here

dades_str = "dbname='ciudaddabd' user='dabduser' host='localhost' password='dabd'"
conn = psycopg2.connect(dades_str)
c = conn.cursor()


def realiza_query(c, q):
	c.execute(q)
	#para guardar en db, dejarlo comentado hasta que quiera simular cosas reales
	#conn.commit()

def crea_parking():
	parking = Parking()
	parking.apply_file('clases/datosMapas/parkingvilanova.osm')
	#print(parking.array_parking)
	for parking in parking.array_parking:
		# Parking (id, lat, lon, precioPorHora) donde el id es P.K.
		realiza_query(c,"INSERT INTO ciudad_parking values(%s,%s,%s,%s);" % (parking[0],parking[1],parking[2],parking[3]))

def crea_calles():
	#En este metodo leeremos de un fichero pero en /home/epsilon/Movurb/ObtenedoresInformacion/pyosmium-parse-streets.py se puede ver como se ha obtenido esto mediante la api
	#de mapquest mapeando todo a cada calle y calculando el bounding box (forma geometrica que constituye la calle con todas sus coordenadas limite)
	with open('clases/TrazasCalles/nombre_calles.txt','r') as calles:
		for calle in calles:
			calle = calle[:-1]
			calle = calle.split("@@@")[0].split('||')
			#calle[1] = calle[1][1:] # eliminamos espacio inicial
			#calle[0] = calle[0][:-1] # eliminamos espacio final
			#Al estar las calles en catalan tenemos que aplicar al fichero previamente el siguiente comando cat nombres_calles.txt | tr "'" .  (sustutimos el caracter ' por el .)
			#ya que sino lo interpreta como string al añadirlo
			realiza_query(c,"""INSERT INTO ciudad_calle(id,nombre) values(%s,'%s');""" % (calle[1],calle[0]))

def crea_horas():
	hora = Hora()
	arrayHoras = hora.getTotalHoras()
	#print(arrayHoras)
	for i in arrayHoras:
		realiza_query(c,"INSERT INTO ciudad_hora values(%s);" % (i))



def crea_parkings_modelo():
	realiza_query(c,"SELECT * FROM ciudad_modelo;")
	arrayModelos = []
	for modelo in c:
		modeloBD = Modelo(modelo[0],modelo[1])
		arrayModelos.append(modeloBD)
	print('Numero de modelos cargados:', len(arrayModelos))

	arrayParkingID = []
	realiza_query(c,"SELECT * FROM ciudad_parking;")
	for parking in c:
		arrayParkingID.append(parking[0])
	id = 1
	for i in range(len(arrayModelos)):
		for parking in arrayParkingID:
			# ParkingModelo (idParkingModelo, idParking) donde el par idParkingModelo, idParking es PRIMARY KEY y, además, estos son FOREIGN KEYS de Modelo y Parking respectivamente.
			realiza_query(c,"INSERT INTO ciudad_parkingModelo (id, idModelo_id, idParking_id) values(%s,%s,%s);" % (id,arrayModelos[i].id,parking))
			id = id + 1


def crea_disponibilidad_parkings():
	print('voy a crear la disponibilidad de parkings')
	realiza_query(c,"SELECT * FROM ParkingModelo;")
	arrayParkingModelos = []
	for parkingModelo in c:
		arrayParkingModelos.append(parkingModelo)

	hora = Hora()
	id = 1
	arrayHoras = hora.getTotalHoras()
	for parkingModelo in arrayParkingModelos:	
		for hora in arrayHoras:
		# Disponible (idParkingModeloHora, idModeloParking, horaParking, estaLibre) donde idParkingModelo, idModeloParking, horaParking serán PRIMARY KEY. Además,  idParkingModelo, idModeloParking son 
		#FOREIGN KEY de ParkingModelo. Y, horaParking es FOREIGN KEY de Hora.
			disponible = randint(0,1) #mi software todavia no detecta/aplica disponibilidad de parking, de ahi el random
			realiza_query(c,"INSERT INTO Disponible values(%s,%s,%s,%s,%s);" % (id,disponible,hora,parkingModelo[0]))
			

def crea_modelos():
	descripcion = "Dia random de VnG"
	modelo = Modelo(1,descripcion)
	realiza_query(c,"INSERT INTO ciudad_modelo (id, descripcion) values(%s,'%s');" % (modelo.id,modelo.descripcion))
	print(modelo)
	descripcion = "Dia medianamente realista de VnG"
	modelo = Modelo(2,descripcion)
	realiza_query(c,"INSERT INTO ciudad_modelo (id, descripcion) values(%s,'%s');" % (modelo.id,modelo.descripcion))
	print(modelo)

def crea_modelos_calles():
	realiza_query(c,"SELECT * FROM ciudad_modelo;")
	arrayModelos = []
	for modelo in c:
		modeloBD = Modelo(modelo[0],modelo[1])
		arrayModelos.append(modeloBD)
	print('Numero de modelos cargados:', len(arrayModelos))
	
	arrayIDCalles = []
	realiza_query(c,"SELECT * FROM ciudad_calle;")
	for calle in c:
		arrayIDCalles.append(calle[1])

	id = 1

	for i in range(len(arrayModelos)):
		for calle in arrayIDCalles:
			# ModeloCalle (idCalle, idModeloCalle) donde el par idCalle, idModeloCalle es PRIMARY KEY. Además, estos a la vez son FOREIGN KEY de Calle y Modelo respectivamente.
			realiza_query(c,"""INSERT INTO ciudad_modelocalle (id,idcalle_id,idmodelo_id) values(%s,%s,%s);""" % (id,calle,arrayModelos[i].id))
			id = id + 1

def crea_trafico():
	#TODO: El resultado obtenido de este trafico no coincide con el que se ha hecho previamente 26k detectado en comparacion de 42k
	#modelo random


	realiza_query(c,"SELECT * FROM ciudad_modelo;")
	arrayModelos = []
	for modelo in c:
		modeloBD = Modelo(modelo[0],modelo[1])
		arrayModelos.append(modeloBD)

	horas = Hora()

	#el modificado es el modelo 1
	trafico = Trafico('clases/diaModificadoVilanova')

	arrayModeloCalles = []
	realiza_query(c,"SELECT * FROM ciudad_modelocalle WHERE idModelo_id=1;")
	for calle in  c:
		arrayModeloCalles.append(calle)

	id = 1
	for hora in horas.getTotalHoras():
		congestionHoraPorCalle = trafico.obten_trafico_hora(hora)
		print(len(congestionHoraPorCalle))
		#print(trafico.array_carreteras)
		for i in range(len(congestionHoraPorCalle)):
			print(arrayModeloCalles[i][0],hora,congestionHoraPorCalle[i])
			realiza_query(c,"INSERT INTO ciudad_trafico values(%s,%s,%s,%s);" % (id, congestionHoraPorCalle[i], hora, arrayModeloCalles[i][0]))
			id = id + 1		
		#break

	arrayModeloCalles = []
	realiza_query(c,"SELECT * FROM ciudad_modelocalle WHERE idModelo_id=2;")
	for calle in  c:
		arrayModeloCalles.append(calle)
	
	trafico = Trafico('clases/diaAproximadoVilanova')
	for hora in horas.getTotalHoras():
		congestionHoraPorCalle = trafico.obten_trafico_hora(hora)
		#print(trafico.array_carreteras)
		for i in range(len(congestionHoraPorCalle)):
			realiza_query(c,"INSERT INTO ciudad_trafico values(%s, %s,%s,%s);" % (id, congestionHoraPorCalle[i], hora, arrayModeloCalles[i][0]))
			id = id + 1
		#break
	
	'''trafico.apunta_trafico_dia('clases/diaModificadoVilanova')
	#modelo aproximado
	trafico = Trafico(8,'Aproximacion')
	trafico.apunta_trafico_dia('clases/testScript-unificado')'''


	# Tráfico (hora,idCalleModelo,idModeloCalleModelo, congestion) donde hora, idCalleModelo, idModeloCalleModelo son PRIMARY KEY. La FOREIGN KEY hora harán referencia a Hora y, idCalleModelo, idModeloCalleModelo harán referencia a ModeloCalle.

def crea_disponibilidad_parkings():
	print('voy a crear la disponibilidad de parkings')
	realiza_query(c,"SELECT * FROM ciudad_parkingmodelo;")
	arrayParkingModelos = []
	for parkingModelo in c:
		arrayParkingModelos.append(parkingModelo)

	id = 1
	hora = Hora()
	arrayHoras = hora.getTotalHoras()
	for parkingModelo in arrayParkingModelos:	
		for hora in arrayHoras:
# Disponible (idParkingModeloHora, idModeloParking, horaParking, estaLibre) donde idParkingModelo, idModeloParking, horaParking serán PRIMARY KEY. Además,  idParkingModelo, idModeloParking son FOREIGN KEY de ParkingModelo. Y, horaParking es FOREIGN KEY de Hora.
			disponible = randint(0,1) #mi software todavia no detecta/aplica disponibilidad de parking, de ahi el random
			estaLibre = False
			if disponible==1:
				estaLibre = True
			realiza_query(c,"INSERT INTO ciudad_disponible values(%s,%s,%s,%s);" % (id, estaLibre, hora, parkingModelo[0]))
			id = id + 1


def insercion_datos():
	print ('INSERCION DATOS')
	pathProgramasObtenedoresInfo = '/home/epsilon/Movurb/ObtenedoresInfoCiudad/'
	pathInfoCiudad = '/home/epsilon/Movurb/InfoCiudades/Vilanova i la Geltru/city_information/'

	#Insercion datos tabla Parking
	print('PARA EL PARKING...')
	crea_parking()

	#Insercion datos Modelo
	print('PARA EL MODELO...')
	crea_modelos()

	#Insercion datos Calle
	print('PARA CALLE...')
	crea_calles()

	#Insercion datos ModeloCalle
	print('PARA MODELOCALLE...')
	crea_modelos_calles()

	#Insercion datos Hora
	print('PARA HORA...')
	#subprocess.run(["sudo","python3",pathProgramasObtenedoresInfo+'generacion_horas.py'])
	crea_horas()

	#Insercion datos ParkingModelo
	print('PARA PARKINGMODELO...')
	crea_parkings_modelo()

	#Inserciond datos Trafico
	print('PARA TRAFICO...')
	#subprocess.run(["sudo","python3",pathProgramasObtenedoresInfo+'calcula_congestion_por_calle_por_hora.py'])
	crea_trafico()

	#Insercion datos Disponible
	print('PARA DISPONIBLE...')
	crea_disponibilidad_parkings()

	#commit


if __name__ == "__main__":
	insercion_datos()
	conn.commit()
	c.close()
	conn.close()


