import xmlparser
import saveload as sl
import graph

def calc_basics_demo(recalc = False):
    if(recalc):
        buildings = xmlparser.getBuildings()
        firestations = xmlparser.getFireStations()
        roads = xmlparser.getRoads()
        coords = xmlparser.getNodesCoords()


        sl.save_obj(firestations, "firestations")
        sl.save_obj(buildings, "buildings")
        sl.save_obj(roads, "roads")
        sl.save_obj(coords, "coords")

        print("demo files recalculated")

    G = graph.GetGraphListWithRead()

    sl.save_obj(G,"adj_list_demo")


def calc_basics_47(recalc=False):
    if(recalc):
        buildings = xmlparser.getBuildings()
        firestations = xmlparser.getFireStations()
        roads = xmlparser.getRoads()
        coords = xmlparser.getNodesCoords()


        sl.save_obj(firestations, "firestations")
        sl.save_obj(buildings, "buildings")
        sl.save_obj(roads, "roads")
        sl.save_obj(coords, "coords")

        print("files recalculated")

    G = graph.GetGraphListWithRead()

    sl.save_obj(G,"adj_list_47")


#calc_basics_demo(True)
calc_basics_47(True)




#fs = sl.load_obj("firestations")
#bld = sl.load_obj("buildings")
#rd = sl.load_obj("roads")
#co = sl.load_obj("coords")

#print(len(co))
