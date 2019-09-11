#Class generated to facilitate the GPS operations
class GPSUtils:

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

