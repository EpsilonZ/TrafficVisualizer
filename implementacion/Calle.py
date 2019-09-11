import osmium as o
import sys
import urllib.request
import json
import uuid


API_KEY = 'YOUR API KEY'

array_ways_encontrados = []

f = open("/home/epsilon/DABD/Practicas/PracticaFinal/implementacion/clases/filtered_traces/nombres_calles.txt","a")
array_carreteras = []

class Calles(o.SimpleHandler):
    def __init__(self):
        super(Calles, self).__init__()

    def way(self, w):
        array_ways_encontrados.append([w.id,w.nodes])
        if 'highway' in w.tags:
            try:
                nombre = w.tags.get('name', '') 
                if(len(nombre)>0):
                    indice,existe = comprueba_si_existe(nombre)
                    if(not existe):
                        array_carreteras.append([nombre,'@@@',w.id])
						
                else:
                    url = 'http://open.mapquestapi.com/geocoding/v1/reverse?key=' + API_KEY + '&location=' + str(w.nodes[0].location.lat) + ',' + \
                    str (w.nodes[0].location.lon) + '&includeRoadMetadata=true&includeNearestIntersection=true'
                    print(url)
                    response = urllib.request.urlopen(url)
                    data = response.read()      # a `bytes` object
                    encoding = response.info().get_content_charset('utf-8')
                    JSON_object = json.loads(data.decode(encoding))
                    nombre = JSON_object["results"][0]["locations"][0]["street"]
                    indice, existe = comprueba_si_existe(nombre)
                    #print(existe)
                    print(nombre)
                    if(len(nombre)<=0):
                        nombre = "NOT FOUND " + str(uuid.uuid4())
                    if(not existe):
                        array_carreteras.append([nombre,'@@@',w.id])

            except o.InvalidLocationError:
                pass

    def relation(self,w):
        if 'highway' in w.tags:
            try:
                #print(len(array_ways_encontrados))
                nombre = w.tags.get('name', '')
                coordenadas_bounding_box = []
                #print (nombre)
                if(len(nombre)<=0):
                    #print ('hey, no tienes nombre')
                    nombre = "NOT FOUND " + str(uuid.uuid4())
                    print (nombre)
                    
                indiceArrayTotal, existe = comprueba_si_existe(nombre)

                if(not existe):
                    array_coordenadas.append([nombre,'@@@',w.id])
            except:
                print ('no hay nombre')

def compruebaIdEnMiLista(identificadorway):
    encontrado = False
    i = 0
    while i < len(array_ways_encontrados) and not encontrado:
        if(array_ways_encontrados[i][0]==identificadorway):
            encontrado = True
        else:
            i = i + 1

    return encontrado,i


def comprueba_si_existe(nombre):
	i = 0
	encontrado = False
	while i < len(array_carreteras) and not encontrado:
		if(array_carreteras[i][0]==nombre):
			encontrado = True
		else:
			i = i + 1

	return i,encontrado

			 
def almacena_en_fichero_limites():

    lineaFichero = ""
    print(len(array_carreteras))
    for i in range(len(array_carreteras)):
        lineaFichero += str(array_carreteras[i][0]) + " " + str(array_carreteras[i][1]) +  " " + str(array_carreteras[i][2]) + "\n"

    lineaFichero = lineaFichero [:-1]
    print(lineaFichero)
    f.write(lineaFichero)
    f.close()

def main(osmfile):
    h = Calles()
    h.apply_file(osmfile, locations=True)
    almacena_en_fichero_limites()
    return 0

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python %s <osmfile>" % sys.argv[0])
        sys.exit(-1)
    main(sys.argv[1])
    exit()
