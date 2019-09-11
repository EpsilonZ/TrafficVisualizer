import osmium as o
import sys
import shapely.wkb as wkblib
import uuid
import random

wkbfab = o.geom.WKBFactory()

class Parking(o.SimpleHandler):

    array_parking = []

    def print_amenity(identificador, amenity, tags, lon, lat):
        name = tags.get('name', '')

        if(len(name)<=0):
           name = "NOT FOUND: " + str(uuid.uuid4())

        '''if('parking' in tags):
           print("%i %f %f parking amenity %-15s %s" % (amenity, lon, lat, tags['parking'], name))
        if('parking:lane:both' in tags):
           print("%i %f %f parking both %-15s %s" % (amenity, lon, lat, tags['parking:lane:both'], name))
        if('parking:lane:left' in tags):
            print("%i %f %f parking left %-15s %s" % (amenity, lon, lat, tags['parking:lane:left'], name))
        if('parking:lane:right' in  tags):
           print("%i %f %f parking right %-15s %s" % (amenity, lon, lat, tags['parking:lane:right'], name))'''

    def way(self,n):
        if es_parking(n.tags):
            valorLon = 0
            valorLat = 0 
            i = 0
            while i < len(n.nodes) and (valorLon == 0 and valorLat == 0):
                try:
                    valorLon = n.nodes[i].location.lon
                    valorLat = n.nodes[i].location.lat
                except:
                    i = i + 1
                    continue
            self.array_parking.append([n.id,valorLat,valorLon,0])
            self.print_amenity(n.id, n.tags, valorLon, valorLat)

    def node(self, n):
        if es_parking(n.tags):
            self.array_parking.append([n.id,n.location.lat,n.location.lon,0])
            self.print_amenity(n.id, n.tags, n.location.lon, n.location.lat)

    def area(self, a):
        if es_parking(a.tags):
            wkb = wkbfab.create_multipolygon(a)
            poly = wkblib.loads(wkb, hex=True)
            centroid = poly.representative_point()
            self.array_parking.append([a.id,centroid.y,centroid.x,0])
            self.print_amenity(a.id, a.tags, centroid.y, centroid.x)

def es_parking(tags):

	es_parking = False
	if(('parking' in tags) or ('parking:lane:both' in tags) or ('parking:lane:left' in tags) or ('parking:lane:right' in tags)):
		es_parking = True
	return es_parking



def main(osmfile):

    handler = Parking()

    handler.apply_file(osmfile)

    return 0

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python %s <ficherosm>" % sys.argv[0])
        sys.exit(-1)

    exit(main(sys.argv[1]))
