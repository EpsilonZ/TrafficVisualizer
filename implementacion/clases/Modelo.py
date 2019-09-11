class Modelo():
	def __init__(self, identificador, descripcionModelo):
		self.id = identificador
		self.descripcion = descripcionModelo

	def __str__(self):
		return str(self.id) + " " + str(self.descripcion)
