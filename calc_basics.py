import xmlparser
import saveload as sl

#buildings = xmlparser.getBuildings()
#firestations = xmlparser.getFireStations()
#roads = xmlparser.getRoads()

#sl.save_obj(firestations, "firestations")
#sl.save_obj(buildings, "buildings")
#sl.save_obj(roads, "roads")

#fs = sl.load_obj("firestations")
#bld = sl.load_obj("buildings")
rd = sl.load_obj("roads")
print(len(rd))
