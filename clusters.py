from scipy.cluster import hierarchy
import matplotlib.pyplot as plt
import numpy as np
import graph
import xmlparser

def Get_k_Clusters(nodes, G, k): # creates a partition into k clusters, result = list of k clusters 
    res = [ [node] for node in nodes]
    dist = {}
    for node in nodes:
        f_nodes = list(set(nodes) - set([node]))
        (D,Parent) = graph.DijkstraWithFinishNodes(G,node, f_nodes)
        graph.GetWeightsDist(D, f_nodes)
        dist[node] = {}
        for n_1 in nodes:
            if n_1 == node:
                continue
            else:
                dist[node][n_1] = D[n_1]
    for node in dist.keys():
        for n_1 in dist[node].keys():
            max_dist = max(dist[node][n_1], dist[n_1][node])
            dist[node][n_1] = max_dist
            dist[n_1][node] = max_dist    
    while len(res) > k:
        min_dist = float('inf')
        cl_1 = []
        cl_2 = []
        new_res = []
        for cluster in res:
            clust_dist = [ 0. for i in res]
            clust_dist[res.index(cluster)] = float('inf')
            for node in cluster:
                for cluster_1 in res:
                    if cluster_1 == cluster:
                        continue
                    else:
                        for node_1 in cluster_1:
                            if dist[node][node_1] >= clust_dist[res.index(cluster_1)]:
                                clust_dist[res.index(cluster_1)] = dist[node][node_1]
            min_clust_dist = min(clust_dist)
            if (min_clust_dist < min_dist):
                min_dist = min_clust_dist
                cl_1 = cluster
                cl_2 = res[clust_dist.index(min_clust_dist)]
        for cluster in res:
            if cluster != cl_1 and cluster != cl_2:
                new_res.append(cluster)
        new_res.append(cl_1 + cl_2)
        res = new_res    
    return res

def Get_Dendro_matr(nodes, G): # creates matrix of linkage for scipy.hierarchy.dendrogram
    res = [ [node] for node in nodes]
    iter_clust = res
    dendro_matr = []
    dist = {}
    for node in nodes:
        f_nodes = list(set(nodes) - set([node]))
        (D,Parent) = graph.DijkstraWithFinishNodes(G,node, f_nodes)
        graph.GetWeightsDist(D, f_nodes)
        dist[node] = {}
        for n_1 in nodes:
            if n_1 == node:
                continue
            else:
                dist[node][n_1] = D[n_1]
    for node in dist.keys():
        for n_1 in dist[node].keys():
            max_dist = max(dist[node][n_1], dist[n_1][node])
            dist[node][n_1] = max_dist
            dist[n_1][node] = max_dist
    while len(res) > 1:
        min_dist = float('inf')
        cl_1 = []
        cl_2 = []
        new_res = []
        for cluster in res:
            clust_dist = [ 0. for i in res]
            clust_dist[res.index(cluster)] = float('inf')
            for node in cluster:
                for cluster_1 in res:
                    if cluster_1 == cluster:
                        continue
                    else:
                        for node_1 in cluster_1:
                            if dist[node][node_1] >= clust_dist[res.index(cluster_1)]:
                                clust_dist[res.index(cluster_1)] = dist[node][node_1]
            min_clust_dist = min(clust_dist)
            if (min_clust_dist < min_dist):
                min_dist = min_clust_dist
                cl_1 = cluster
                cl_2 = res[clust_dist.index(min_clust_dist)]
        for cluster in res:
            if cluster != cl_1 and cluster != cl_2:
                new_res.append(cluster)
        new_res.append(cl_1 + cl_2)
        iter_clust.append(cl_1 + cl_2)
        dendro_matr.append([iter_clust.index(cl_1), iter_clust.index(cl_2), min_clust_dist, len(iter_clust[-1])])
        res = new_res    
    return np.matrix(dendro_matr)


def Get_Clusters(nodes, G): # creates a partition into 5,3 and 2 clusters, also creates matrix of linkage for scipy.hierarchy.dendrogram
    res_5 = [ [node] for node in nodes]
    iter_clust = res_5
    dendro_matr = []
    dist = {}
    for node in nodes:
        f_nodes = list(set(nodes) - set([node]))
        (D,Parent) = graph.DijkstraWithFinishNodes(G,node, f_nodes)
        graph.GetWeightsDist(D, f_nodes)
        dist[node] = {}
        for n_1 in nodes:
            if n_1 == node:
                continue
            else:
                dist[node][n_1] = D[n_1]
    for node in dist.keys():
        for n_1 in dist[node].keys():
            max_dist = max(dist[node][n_1], dist[n_1][node])
            dist[node][n_1] = max_dist
            dist[n_1][node] = max_dist
    while len(res_5) > 5:
        min_dist = float('inf')
        cl_1 = []
        cl_2 = []
        new_res = []
        for cluster in res_5:
            clust_dist = [ 0. for i in res_5]
            clust_dist[res_5.index(cluster)] = float('inf')
            for node in cluster:
                for cluster_1 in res_5:
                    if cluster_1 == cluster:
                        continue
                    else:
                        for node_1 in cluster_1:
                            if dist[node][node_1] >= clust_dist[res_5.index(cluster_1)]:
                                clust_dist[res_5.index(cluster_1)] = dist[node][node_1]
            min_clust_dist = min(clust_dist)
            if (min_clust_dist < min_dist):
                min_dist = min_clust_dist
                cl_1 = cluster
                cl_2 = res_5[clust_dist.index(min_clust_dist)]
        for cluster in res_5:
            if cluster != cl_1 and cluster != cl_2:
                new_res.append(cluster)
        new_res.append(cl_1 + cl_2)
        iter_clust.append(cl_1 + cl_2)
        dendro_matr.append([iter_clust.index(cl_1), iter_clust.index(cl_2), min_clust_dist, len(iter_clust[-1])])
        res_5 = new_res
    res_3 = res_5
    while len(res_3) > 3:
        min_dist = float('inf')
        cl_1 = []
        cl_2 = []
        new_res = []
        for cluster in res_3:
            clust_dist = [ 0. for i in res_3]
            clust_dist[res_3.index(cluster)] = float('inf')
            for node in cluster:
                for cluster_1 in res_3:
                    if cluster_1 == cluster:
                        continue
                    else:
                        for node_1 in cluster_1:
                            if dist[node][node_1] >= clust_dist[res_3.index(cluster_1)]:
                                clust_dist[res_3.index(cluster_1)] = dist[node][node_1]
            min_clust_dist = min(clust_dist)
            if (min_clust_dist < min_dist):
                min_dist = min_clust_dist
                cl_1 = cluster
                cl_2 = res_3[clust_dist.index(min_clust_dist)]
        for cluster in res_3:
            if cluster != cl_1 and cluster != cl_2:
                new_res.append(cluster)
        new_res.append(cl_1 + cl_2)
        iter_clust.append(cl_1 + cl_2)
        dendro_matr.append([iter_clust.index(cl_1), iter_clust.index(cl_2), min_clust_dist, len(iter_clust[-1])])
        res_3 = new_res
    res_2 = res_3
    while len(res_2) > 2:
        min_dist = float('inf')
        cl_1 = []
        cl_2 = []
        new_res = []
        for cluster in res_2:
            clust_dist = [ 0. for i in res_2]
            clust_dist[res_2.index(cluster)] = float('inf')
            for node in cluster:
                for cluster_1 in res_2:
                    if cluster_1 == cluster:
                        continue
                    else:
                        for node_1 in cluster_1:
                            if dist[node][node_1] >= clust_dist[res_2.index(cluster_1)]:
                                clust_dist[res_2.index(cluster_1)] = dist[node][node_1]
            min_clust_dist = min(clust_dist)
            if (min_clust_dist < min_dist):
                min_dist = min_clust_dist
                cl_1 = cluster
                cl_2 = res_2[clust_dist.index(min_clust_dist)]
        for cluster in res_2:
            if cluster != cl_1 and cluster != cl_2:
                new_res.append(cluster)
        new_res.append(cl_1 + cl_2)
        iter_clust.append(cl_1 + cl_2)
        dendro_matr.append([iter_clust.index(cl_1), iter_clust.index(cl_2), min_clust_dist, len(iter_clust[-1])])
        res_2 = new_res
    min_dist = float('inf')
    cl_1 = []
    cl_2 = []
    for cluster in res_2:
        clust_dist = [ 0. for i in res_2]
        clust_dist[res_2.index(cluster)] = float('inf')
        for node in cluster:
            for cluster_1 in res_2:
                if cluster_1 == cluster:
                    continue
                else:
                    for node_1 in cluster_1:
                        if dist[node][node_1] >= clust_dist[res_2.index(cluster_1)]:
                            clust_dist[res_2.index(cluster_1)] = dist[node][node_1]
        min_clust_dist = min(clust_dist)
        if (min_clust_dist < min_dist):
            min_dist = min_clust_dist
            cl_1 = cluster
            cl_2 = res_2[clust_dist.index(min_clust_dist)]
    dendro_matr.append([iter_clust.index(cl_1), iter_clust.index(cl_2), min_clust_dist, len(cl_1+cl_2)])    
    return res_5, res_3, res_2, np.matrix(dendro_matr)



def Find_Centers(clusters, G): # return centers of clusters
    res = []
    coords = xmlparser.getNodesCoords()
    for cluster in clusters:
        sum_lat = 0.
        sum_lon = 0.
        for node in cluster:
            sum_lat += float(coords[node][0])
            sum_lon += float(coords[node][1])
        obj_coords = (sum_lat/len(cluster), sum_lon/len(cluster))
        result = '-'
        min_dist = float('inf')
        for node in G:
            node_coords = coords[node]
            distance = 1000000*((float(node_coords[0])-obj_coords[0])**2 + (float(node_coords[1])-obj_coords[1])**2)
            if (distance < min_dist):
                min_dist = distance
                result = node
        res.append(result)
    return res
