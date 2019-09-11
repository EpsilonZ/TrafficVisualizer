class Hora:
	def __init__(self):
		self.horaBase = 6
		self.horafin = 24

	def getTotalHoras(self):
		arrayTotal = []
		indice = self.horaBase
		while(indice<=self.horafin):
			arrayTotal.append(indice)
			indice+=1
		return arrayTotal
