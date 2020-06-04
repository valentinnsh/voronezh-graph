import xmlparser
import random
import saveload

def GetTree(finish_nodes, parents): # finish nodes from GetBuildingObjects, parents - Parent from Djikstra
    res = []
    for fnode in finish_nodes:
        curr_node = fnode
        parent_node = parents[fnode]
        while parent_node != '-':
            edge = (parent_node, curr_node)
            if edge not in res:
                res.append(edge)
            else: 
                break
            curr_node = parent_node
            parent_node = parents[parent_node]
    return res # list of edges (in turple)

def GetSumOfTree(edges, adj_list): # return sum of tree; edges - from GetTree, adj_list from GetGraphList
    res = 0
    for edge in edges:
        for node in adj_list[edge[0]]:
            if node[0] == edge[1]:
                res += node[1]
                break
    return res

def  GetMaxDist(Dist_list, nodes): # return max_dist (m_d) from root and nodes with this dist; Dist_list from Djikstra, nodes from GetBuildingObjects
    m_d = 0.
    res = []
    for node in nodes:
        if Dist_list[node] > m_d:
            m_d = Dist_list[node]
    for node in nodes:
        if Dist_list[node] == m_d:
            res.append(node)        
    return m_d, res

def  GetMinDist(Dist_list, nodes): # return min_dist (m_d) from root and nodes with this dist; with Dist_list from Djikstra, nodes from GetBuildingObjects
    m_d = float('inf')
    res = []
    for node in nodes:
        if Dist_list[node] < m_d:
            m_d = Dist_list[node]
    for node in nodes:
        if Dist_list[node] == m_d:
            res.append(node)        
    return m_d, res

def  GetNodes_inDist(Dist_list, nodes, dist): # return nodes which distance from root < dist; Dist_list from Djikstra, nodes from GetBuildingObjects, dist - metr
    res = []
    for node in nodes:
        if Dist_list[node] < dist:
            res.append(node)       
    return res

def GetSumMaxDist(Dist_list,nodes): # return sum of dist from root to nodes; Dist_list from Djikstra, nodes from GetBuildingObjects
    m_d = 0
    for node in nodes:
        m += Dist_list[node]
    return m_d

def GetGraphList():
    graph_list = {}
    roads = xmlparser.getRoads()
    coords = xmlparser.getNodesCoords()
    buildings = xmlparser.getBuildings() + xmlparser.getFireStations()
    print('phase1')
    for road in roads:
        oneway = False
        if 'oneway' in road.keys():
            if road['oneway'] == 'yes':
                oneway = True
        nodes = road['nodes']
        for node in nodes:
            if node not in graph_list.keys():
                graph_list[node] = []
        for i in range(len(nodes)):
            if (i < len(nodes) - 1):
                node1_coords = coords[nodes[i]]
                node2_coords = coords[nodes[i + 1]]
                distance = round(1000000*((float(node1_coords[0])-float(node2_coords[0]))**2 + (float(node1_coords[1])-float(node2_coords[1]))**2), 4)
                graph_list[nodes[i]].append((nodes[i+1],distance))
                if not oneway:
                    graph_list[nodes[i+1]].append((nodes[i],distance))
    print('phase2')
    road_list = graph_list.copy()
    for building in buildings:
        graph_list[building['id']] = []
        node1_coords = coords[building['id']]
        nearest_node = '-'
        min_dist = float('inf')
        for node in road_list:
            node_coords = coords[node]
            distance = 1000000*((float(node1_coords[0])-float(node2_coords[0]))**2 + (float(node1_coords[1])-float(node2_coords[1]))**2)
            if (distance < min_dist):
                min_dist = distance
                nearest_node = node
                node2_coords = node_coords       
        min_dist = round(min_dist, 4)
        graph_list[building['id']].append((nearest_node,min_dist))
        graph_list[nearest_node].append((building['id'], min_dist))

    build_nodes = [ building['id'] for building in buildings]
    print('phase3')
    # delete vertexes
    for v in road_list.keys():
        if len(graph_list[v]) <=2:
            connect = False
            for vert in graph_list[v]:
                if vert[0] in build_nodes:
                    connect = True
                    break
            if connect == False:
                # oneway
                if len(graph_list[v]) == 1:
                    vert_in = []
                    vert_out = [ vert[0] for vert in graph_list[v]]
                    for vert in graph_list.keys():
                        if v in [ v_out[0] for v_out in graph_list[vert]]:
                            vert_in.append(vert)
                    if len(vert_in) == len(vert_out) and set(vert_in) != set(vert_out):
                        l = [ v_out[0] for v_out in graph_list[vert_in[0]]]
                        index = l.index(v)
                        node1_coords = coords[vert_in[0]]
                        node2_coords = coords[vert_out[0]]
                        distance = round(1000000*((float(node1_coords[0])-float(node2_coords[0]))**2 + (float(node1_coords[1])-float(node2_coords[1]))**2), 4)
                        graph_list[vert_in[0]].append((vert_out[0], distance))
                        graph_list[vert_in[0]].remove(graph_list[vert_in[0]][index])
                        del graph_list[v]
                # twoways
                elif len(graph_list[v]) == 2:
                    vert_in = []
                    vert_out = [ vert[0] for vert in graph_list[v]]
                    for vert in graph_list.keys():
                        if v in [ v_out[0] for v_out in graph_list[vert]]:
                            vert_in.append(vert)
                    if len(vert_in) == len(vert_out) and set(vert_in) == set(vert_out):
                        v1 = vert_in[0]
                        v2 = vert_in[1]
                        l1 = [ v_out[0] for v_out in graph_list[v1]]
                        l2 = [ v_out[0] for v_out in graph_list[v2]]
                        index1 = l1.index(v)
                        index2 = l2.index(v)
                        node1_coords = coords[v1]
                        node2_coords = coords[v2]
                        distance = round(1000000*((float(node1_coords[0])-float(node2_coords[0]))**2 + (float(node1_coords[1])-float(node2_coords[1]))**2), 4)
                        graph_list[v1].append((v2, distance))
                        graph_list[v2].append((v1, distance))
                        graph_list[v1].remove(graph_list[v1][index1])
                        graph_list[v2].remove(graph_list[v2][index2])
                        del graph_list[v]              
    print('graph is builded')
    return graph_list


def GetGraphListWithRead():
    graph_list = {}
    roads = saveload.load_obj('roads')
    coords = saveload.load_obj('coords')
    buildings = saveload.load_obj('buildings') + saveload.load_obj('firestations')
    print('phase1')
    for road in roads:
        oneway = False
        if 'oneway' in road.keys():
            if road['oneway'] == 'yes':
                oneway = True
        nodes = road['nodes']
        for node in nodes:
            if node not in graph_list.keys():
                graph_list[node] = []
        for i in range(len(nodes)):
            if (i < len(nodes) - 1):
                node1_coords = coords[nodes[i]]
                node2_coords = coords[nodes[i + 1]]
                distance = round(1000000*((float(node1_coords[0])-float(node2_coords[0]))**2 + (float(node1_coords[1])-float(node2_coords[1]))**2), 4)
                graph_list[nodes[i]].append((nodes[i+1],distance))
                if not oneway:
                    graph_list[nodes[i+1]].append((nodes[i],distance))
    print('phase2')
    road_list = graph_list.copy()
    for building in buildings:
        graph_list[building['id']] = []
        node1_coords = coords[building['id']]
        nearest_node = '-'
        min_dist = float('inf')
        for node in road_list:
            node_coords = coords[node]
            distance = 1000000*((float(node1_coords[0])-float(node2_coords[0]))**2 + (float(node1_coords[1])-float(node2_coords[1]))**2)
            if (distance < min_dist):
                min_dist = distance
                nearest_node = node
                node2_coords = node_coords       
        min_dist = round(min_dist, 4)
        graph_list[building['id']].append((nearest_node,min_dist))
        graph_list[nearest_node].append((building['id'], min_dist))

    build_nodes = [ building['id'] for building in buildings]
    print('phase3')
    # delete vertexes
    for v in road_list.keys():
        if len(graph_list[v]) <=2:
            connect = False
            for vert in graph_list[v]:
                if vert[0] in build_nodes:
                    connect = True
                    break
            if connect == False:
                # oneway
                if len(graph_list[v]) == 1:
                    vert_in = []
                    vert_out = [ vert[0] for vert in graph_list[v]]
                    for vert in graph_list.keys():
                        if v in [ v_out[0] for v_out in graph_list[vert]]:
                            vert_in.append(vert)
                    if len(vert_in) == len(vert_out) and set(vert_in) != set(vert_out):
                        l = [ v_out[0] for v_out in graph_list[vert_in[0]]]
                        index = l.index(v)
                        node1_coords = coords[vert_in[0]]
                        node2_coords = coords[vert_out[0]]
                        distance = round(1000000*((float(node1_coords[0])-float(node2_coords[0]))**2 + (float(node1_coords[1])-float(node2_coords[1]))**2), 4)
                        graph_list[vert_in[0]].append((vert_out[0], distance))
                        graph_list[vert_in[0]].remove(graph_list[vert_in[0]][index])
                        del graph_list[v]
                # twoways
                elif len(graph_list[v]) == 2:
                    vert_in = []
                    vert_out = [ vert[0] for vert in graph_list[v]]
                    for vert in graph_list.keys():
                        if v in [ v_out[0] for v_out in graph_list[vert]]:
                            vert_in.append(vert)
                    if len(vert_in) == len(vert_out) and set(vert_in) == set(vert_out):
                        v1 = vert_in[0]
                        v2 = vert_in[1]
                        l1 = [ v_out[0] for v_out in graph_list[v1]]
                        l2 = [ v_out[0] for v_out in graph_list[v2]]
                        index1 = l1.index(v)
                        index2 = l2.index(v)
                        node1_coords = coords[v1]
                        node2_coords = coords[v2]
                        distance = round(1000000*((float(node1_coords[0])-float(node2_coords[0]))**2 + (float(node1_coords[1])-float(node2_coords[1]))**2), 4)
                        graph_list[v1].append((v2, distance))
                        graph_list[v2].append((v1, distance))
                        graph_list[v1].remove(graph_list[v1][index1])
                        graph_list[v2].remove(graph_list[v2][index2])
                        del graph_list[v]              
    print('graph is builded')
    return graph_list


def Dijkstra(G, start_node): # Djikstra alg, return patents and dist for each node in graph list (G) from start_node 
    dist = {}
    parent = {}
    not_matched = G.copy()
    for node in G:
        dist[node] = float('inf')
        parent[node] = '-'
    dist[start_node] = 0
    while (len(not_matched) > 0):
        min_dist = float('inf')
        for node in not_matched:
            if (dist[node] <= min_dist):
                curr_node = node
                min_dist = dist[node]
        for node in G[curr_node]:
            if (dist[node[0]] > dist[curr_node] + node[1]):
                dist[node[0]] = dist[curr_node] + node[1]
                parent[node[0]] = curr_node
        del not_matched[curr_node]
    return (dist, parent)

def DijkstraWithFinishNodes(G, start_node, finish_nodes): # Djikstra alg, return patents and dist for each node in graph list (G) from start_node 
    dist = {}
    parent = {}
    not_matched = G.copy()
    f_nodes = finish_nodes[:]
    for node in G:
        dist[node] = float('inf')
        parent[node] = '-'
    dist[start_node] = 0
    while (len(f_nodes) > 0):
        min_dist = float('inf')
        for node in not_matched:
            if (dist[node] <= min_dist):
                curr_node = node
                min_dist = dist[node]
        for node in G[curr_node]:
            if (dist[node[0]] > dist[curr_node] + node[1]):
                dist[node[0]] = dist[curr_node] + node[1]
                parent[node[0]] = curr_node
        del not_matched[curr_node]
        if curr_node in f_nodes:
            f_nodes.remove(curr_node)
    return (dist, parent)



