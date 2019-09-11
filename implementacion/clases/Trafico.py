import datetime
from datetime import timedelta
import numpy as np
import sys

class Trafico():

	def __init__(self,pathFichero):
		#self.horaTrafico = horaAsignada
		#self.idModelo = modelo
		self.pathHastaTraza = pathFichero
		self.horaBase = 6
		self.minutosBase = 0
		self.segundosBase = 0
		self.array_carreteras = []
		self.array_carreterasleftRightBottomTop = []
		self.carretera_id = []
		self.carga_carreteras()


	def carga_carreteras(self):
		with open("/home/epsilon/DABD/Practicas/PracticaFinal/implementacion/django_dabd/clases/TrazasCalles/limitesCarreteraTraducidosVilanovaILaGeltru.txt","r") as ficheroCarreteras:
			first = False		
			for carretera in ficheroCarreteras:
				totalDividido = carretera.split("@@@")
				#print(totalDividido)
				nombreCarretera = totalDividido[0].split("||")[0] #le quitamos el espacio del final al nombre
				carretera = totalDividido[1].split(" ")
				#Quitamos el primer elemento que hace referencia al id de la carretera			
				self.carretera_id.append(nombreCarretera)			
				#carretera.pop(0)
				#Pasamos a int el array
				carretera = list(map(int,carretera))

				#Agrupamos en parejas de dos el array para juntar en x,y las coordenadas
				n = 2
				carretera = [ carretera[i:i+n] for i in range(0, len(carretera), n) ]
				self.array_carreteras.append(carretera)
				max_x = carretera[0][0]
				min_x = carretera[0][0]
				max_y = carretera[0][1]
				min_y = carretera[0][1]
				for indice in range(len(carretera)):
					if(carretera[indice][0] > max_x):
						max_x = carretera[indice][0]
					if(carretera[indice][0] < min_x):
						min_x = carretera[indice][0]
					if(carretera[indice][1] > max_y):
						max_y = carretera[indice][1]
					if(carretera[indice][1] < min_y):
						min_y = carretera[indice][1]

				#print ("------------------------")
				#print (min_x,max_x,min_y,max_y)
				#print (carretera)
				#print ("------------------------")
				self.array_carreterasleftRightBottomTop.append([min_x,max_x,min_y,max_y])
				


	def esta_dentro_carretera(self,x,y,poly):
	# Funcion para detectar si un punto esta dentro de un poligono --> https://wrf.ecse.rpi.edu//Research/Short_Notes/pnpoly.html

		"""
		x, y -- x and y coordinates of point
		poly -- a list of tuples [(x, y), (x, y), ...]
		"""
		num = len(poly)
		i = 0
		j = num - 1
		c = False
		for i in range(num):
		    if ((poly[i][1] > y) != (poly[j][1] > y)) and \
		            (x < poly[i][0] + (poly[j][0] - poly[i][0]) * (y - poly[i][1]) /
		                              (poly[j][1] - poly[i][1])):
		        c = not c
		    j = i
		return c 


	def compruebaCercania(self,numCarretera,x,y):

		estaCerca = False
		#array_carreteras_maximo_minimo el [0] es el max y el [1] es el min
		if((self.array_carreterasleftRightBottomTop[numCarretera][0] <= x and self.array_carreterasleftRightBottomTop[numCarretera][1] >= x and \
			self.array_carreterasleftRightBottomTop[numCarretera][2] <= y and self.array_carreterasleftRightBottomTop[numCarretera][3] >= y)):

			estaCerca = True

		return estaCerca

	def detecta_en_que_carretera(self,x,y):

		carreteraEncontrada = False
		contadorCarreteras = 0
		while(not carreteraEncontrada and contadorCarreteras<len(self.array_carreteras)):
			#TODO: Optimizacion. Comparar si la diferencia es muy grande respecto las coordenadas y si lo es, pasar a la siguiente		
			estaCerca = self.compruebaCercania (contadorCarreteras,x,y)
			if(estaCerca):
				carreteraEncontrada = self.esta_dentro_carretera(x,y,self.array_carreteras[contadorCarreteras])
			if(not carreteraEncontrada):
				contadorCarreteras += 1

		valorReturn = contadorCarreteras
		if(not carreteraEncontrada):
			valorReturn = -1

		#else:
		#	print('Punto x,y:', x, y, 'no encontrada la carretera a la que corresponde')

		return valorReturn


	def apunta_trafico_instante(self,instante):

		instante = instante.split(" ")
		#La estructura del fichero es x1 y1 color1 x2 y2 color2 ... xn yn colorn\n
		i = 0			
		#print(len(self.array_carreteras))
		#print(len(self.carretera_id))
		#print(len(self.array_carreterasleftRightBottomTop))

		arrayTraficoPorCarretera = [0] * len(self.array_carreteras)
		#print (array_carreteras_maximo_minimo)
		
		while i < len(instante):
			numCarretera = self.detecta_en_que_carretera(int(float(instante[i])),int(float(instante[i+1])))
			#print(numCarretera)
			i+=3
			#print(numCarretera)
			if(numCarretera!=-1):
				#print(arrayTraficoPorCarretera[numCarretera])
				arrayTraficoPorCarretera[numCarretera]+=1

		#print(arrayTraficoPorCarretera)

		for i in range(len(self.array_carreteras)):
			print(self.carretera_id[i],":",arrayTraficoPorCarretera[i])
		
		print("Trafico total detectado:",sum(arrayTraficoPorCarretera))

		return arrayTraficoPorCarretera

	def actualiza_hora(self):
		self.segundosBase = self.segundosBase + 10
		if(self.segundosBase==60):
			self.segundosBase = 0
			self.minutosBase = self.minutosBase + 1
			if(self.minutosBase==60):
				self.minutosBase = 0
				self.horaBase = self.horaBase + 1

	def apunta_trafico_dia(self,hora):
		#print(self.array_carreteras)
		#print(self.carretera_id)
		#print(self.array_carreterasleftRightBottomTop)
		with open(self.pathHastaTraza,"r") as trazaTotal:
			contador = 0
			for instante in trazaTotal:
				contador = contador + 1
				#print(self.horaBase,self.minutosBase,self.segundosBase)
				if(hora==self.horaBase and self.segundosBase==0 and self.minutosBase==0):
					return self.apunta_trafico_instante(instante)
				self.actualiza_hora()

	def obten_trafico_hora(self, hora):
		return self.apunta_trafico_dia(hora)

if __name__ == "__main__":

	if(len(sys.argv)<2):
		print("Es necesario que especifiques la traza del modelo de dia. Usage: python3 Trafico.py pathHastaTraza")
		exit(1)
	trafico = Trafico(sys.argv[1])
	trafico.carga_carreteras()
	print(trafico.obten_trafico_hora(6))

