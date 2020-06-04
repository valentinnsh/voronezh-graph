import xmlparser
import graph
import random
import clusters
import saveload as sl
from scipy.cluster import hierarchy
import matplotlib.pyplot as plt
import numpy as np


def GetBuildingsObjects(sd, b_n, o_n):
    random.seed(sd)
    builds = sl.load_obj('buildings')
    objects = sl.load_obj('firestations')
    builds_choice = random.sample(builds, b_n)
    objects_choice = random.sample(objects, o_n)
    res_builds = [ b['id'] for b in builds_choice ]
    res_objects = [ o['id'] for o in objects_choice]
    return res_builds, res_objects

def GetMatr(G):
    nodes = [node for node in G.keys()]
    res = [[0 for node2 in nodes] for node1 in nodes]
    for n_1 in nodes:
        for n_2 in G[n_1]:
            res[nodes.index(n_1)][nodes.index(n_2[0])] = n_2[1] 
    return np.matrix(res)


def main():
    #random.seed(5)
    print(xmlparser.getHighway())
    g = graph.GetGraphList()
    print(g)
    (a_id,b_id) = GetBuildingsObjects(4,8,2)
    print("sample of houses:")    
    print(a_id)
    print(b_id)
    print('Big Dijkstra:')
    (D,Parent) = graph.Dijkstra(g,b_id[0])
    tree = graph.GetTree(a_id, Parent)
    print("tree from b_id[0] (one of the objects) to a_id (sample of houses):")    
    print(tree)
    print("length of previous tree:")
    print(graph.GetSumOfTree(tree,g))
    (m_d, m_nodes) = graph.GetMaxDist(D, a_id)
    print("max dist from root in tree :")
    print(m_d)
    print("node with max dist from root in tree:")
    print(m_nodes)

    print('Dijkstra with f_nodes:')
    (D,Parent) = graph.DijkstraWithFinishNodes(g,b_id[0],a_id)
    print(a_id)
    tree = graph.GetTree(a_id, Parent)
    print("tree from b_id[0] (one of the objects) to a_id (sample of houses):")    
    print(tree)
    print("length of previous tree:")
    print(graph.GetSumOfTree(tree,g))
    (m_d, m_nodes) = graph.GetMaxDist(D, a_id)
    print("max dist from root in tree :")
    print(m_d)
    print("node with max dist from root in tree:")
    print(m_nodes)
    (res_5, res_3, res_2, dendro_matr) = clusters.Get_Clusters(a_id, g)
    print("5 clusters:")
    print(res_5)
    print(clusters.Get_k_Clusters(a_id,g,5))
    print("3 clusters:")
    print(res_3)
    print("2 clusters:")
    print(res_2)
    print("centers of 5 clusters")
    print(clusters.Find_Centers(res_5, g))
    plt.figure()
    dn = hierarchy.dendrogram(clusters.Get_Dendro_matr(a_id, g))
    plt.savefig('foo.pdf')


if __name__ == "__main__":
    main()