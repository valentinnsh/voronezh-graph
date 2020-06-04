import xml.etree.ElementTree as ET 

tree = ET.parse('planet47mb.osm')
db = tree.getroot()


# save to files

def getNodesCoords():   
    res = { row.attrib['id'] : (row.attrib['lat'], row.attrib['lon']) for row in db.iter('node')}
    return res


def getBuildings():
    buildings = []
    for row in db.iter('way'):
        condition = False
        building = {}
        for element in row.iter('tag'):
            building[element.attrib['k']] = element.attrib['v']
            if element.attrib['k'] == 'building' and (element.attrib['v'] == 'house' or element.attrib['v'] == 'apartments'):
                condition = True
        if condition:
            for element in row.iter('nd'):
                building['id'] = element.attrib['ref']
                break
            buildings.append(building)
    return buildings

def getFireStations():
    buildings = []
    for row in db.iter('way'):
        condition = False
        building = {}
        for element in row.iter('tag'):
            building[element.attrib['k']] = element.attrib['v']
            if element.attrib['k'] == 'amenity' and element.attrib['v'] == 'fire_station':
                condition = True
        if condition:
            for element in row.iter('nd'):
                building['id'] = element.attrib['ref']
                break
            buildings.append(building)
    return buildings

def getRoads():
    roads = []
    road_types = ['living_street', 'motorway', 'primary',  'primary_link', 'residential', 'road', 'secondary', 'service', 'services' 'secondary_link', 'tertiary', 'tertiary_link', 'trunk', 'trunk_link', 'unclassified']
    for row in db.iter('way'):
        condition = False
        road = {}
        for element in row.iter('tag'):
            road[element.attrib['k']] = element.attrib['v']
            if element.attrib['k'] == 'highway' and (element.attrib['v'] in road_types):
                condition = True
        if condition:
            road['nodes'] = []
            for element in row.iter('nd'):
                road['nodes'].append(element.attrib['ref'])
            roads.append(road)
    return roads

# seconndary, just for explore

def getHighway():
    res = []
    for row in db.iter('way'):
        for element in row.iter('tag'):
            if element.attrib['k'] == 'highway' and element.attrib['v'] not in res:
                print(element.attrib['v'])
                res.append(element.attrib['v'])
    return res

def getAllBuildings():
    buildings = []
    for row in db.iter('way'):
        condition = False
        building = {}
        for element in row.iter('tag'):
            building[element.attrib['k']] = element.attrib['v']
            if element.attrib['k'] == 'building':
                condition = True
        if condition:
            for element in row.iter('nd'):
                building['id'] = element.attrib['ref']
                break
            buildings.append(building)
    return buildings

def getBuildingsByType(type = ''):
    buildings = []
    for row in db.iter('way'):
        condition = False
        building = {}
        for element in row.iter('tag'):
            building[element.attrib['k']] = element.attrib['v']
            if element.attrib['k'] == 'building' and element.attrib['v'] == type:
                condition = True
        if condition:
            for element in row.iter('nd'):
                building['id'] = element.attrib['ref']
                break
            buildings.append(building)
    return buildings