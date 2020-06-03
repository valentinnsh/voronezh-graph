import xmlparser
import saveload as sl

#buildings = xmlparser.getBuildings()
#firestations = xmlparser.getFireStations()
#roads = xmlparser.getRoads()
coords = xmlparser.getNodesCoords()


#sl.save_obj(firestations, "firestations")
#sl.save_obj(buildings, "buildings")
#sl.save_obj(roads, "roads")
sl.save_obj(coords, "coords")

#fs = sl.load_obj("firestations")
#bld = sl.load_obj("buildings")
#rd = sl.load_obj("roads")
co = sl.load_obj("coords")

print(len(co))
