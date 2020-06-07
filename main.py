import xmlparser
import graph
import random
import clusters
import saveload as sl
from scipy.cluster import hierarchy
import matplotlib.pyplot as plt
import numpy as np
import argparse

def GetBuildingsObjects(sd, b_n, o_n): #sd - seed(integer), buildings number, o- firestation number
    random.seed(sd)
    builds = sl.load_obj('buildings')
    objects = sl.load_obj('firestations')
    builds_choice = random.sample(builds, b_n)
    objects_choice = random.sample(objects, o_n)
    res_builds = [ b['id'] for b in builds_choice ]
    res_objects = [ o['id'] for o in objects_choice]
    return res_builds, res_objects

def GetInfo(id):
    builds = sl.load_obj('buildings')
    firestations = sl.load_obj('firestations')
    roads = sl.load_obj('roads')
    for build in builds:
        if build['id'] == id:
            res = build
    for firestation in firestations:
        if firestation['id'] == id:
            res = firestation
    for road in roads:
        for nd in road['nodes']:
            if nd == id:
                res = road
    return res


def GetMatr(G):
    nodes = [node for node in G.keys()]
    res = [[0 for node2 in nodes] for node1 in nodes]
    for n_1 in nodes:
        for n_2 in G[n_1]:
            res[nodes.index(n_1)][nodes.index(n_2[0])] = n_2[1]
    return np.matrix(res)


def old_main():
    #random.seed(5)
    print(GetInfo('563305885'))
    '''
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
    '''


def main(args):
    G = sl.load_obj("adj_list_47")

    # Show fire stations
    if(args.show_fs):
        firestations = sl.load_obj("firestations")
        for station in firestations:
            print(station['id'], station['name'])

    # Get Info By ID
    if(args.info is not None):
        try:
            res = GetInfo(args.info)
            for i in res:
                print(i, res[i])

        except UnboundLocalError:
            print("Wrong id. Check it and try again.")
        except:
            print("Oops, something went wrong")


    #First half of task.
    if(args.pick_fs_and_bds is not None):

        m = args.pick_fs_and_bds[0]
        n = args.pick_fs_and_bds[1]
        # Pick random m firestations and n buildings
        builds, stations = GetBuildingsObjects(args.pick_fs_and_bds[2],n ,m)

        # Now to analyse the distance values we have t orun DijkstraWithFinishNodes for all stations and all buildings

        res_builds = {}
        res_stations = {}
        mindist_from_builds = {}
        mindist_from_stations = {}

        if(args.no_recalc_values is None):
            for b in builds:
                res_builds[b] = graph.DijkstraWithFinishNodes(G, b, stations)
                dist, minfb = graph.GetMinDist(res_builds[b][0], stations)
                mindist_from_builds[b] = (dist,minfb)

                print("Для дома c id = ", b, " ближайшая пожарная станция - ", GetInfo(minfb[0])['name'], " id = ", minfb)
                print("-----------------------------------------------------------------------------------------------------------")


            print("\n")
            for st in stations:
                res_stations[st] = graph.DijkstraWithFinishNodes(G,st, builds)
                dist, minfs = graph.GetMinDist(res_stations[st][0], builds)
                mindist_from_stations[st] = (dist,minfs)

                print("Для пожарной станции ", GetInfo(st)["name"], " id = ", st, " ближайший дом c id = ", minfs)
                print("-----------------------------------------------------------------------------------------------------------")

            sl.save_obj(res_builds,"res_builds")
            sl.save_obj(res_stations, "res_stations")
            sl.save_obj(mindist_from_stations, "mindist_from_stations")
            sl.save_obj(mindist_from_builds, "mindist_from_builds")

        else:
            res_builds = sl.load_obj("res_builds")
            res_stations = sl.load_obj("res_stations")
            mindist_from_builds = sl.load_obj("mindist_from_builds")
            mindist_from_stations = sl.load_obj("mindist_from_stations")


        # Ищем минимум расстояния туда+обратно
        if(args.both_sides is not None):
            for b in builds:
                min_dist_sum = float('inf')
                closest_station = None
                for st in stations:
                    if(min_dist_sum > res_stations[st][0][b]+res_builds[b][0][st]):
                        min_dist_sum = res_stations[st][0][b]+res_builds[b][0][st]
                        closest_station = st

                print(f"Для дома с id = {b} ближайшая(по сумме туда-обратно) пожарная станция {GetInfo(closest_station)['name']}")


        #Для какого объекта инфраструктуры сумма кратчайших расстояний от него до всех домов минимальна.
        if(args.sum_of_paths is not None):
            min_of_sum = float('inf')
            minel = None
            for st in stations:
                currsum = 0
                for s in res_stations[st][0]:
                    currsum+=res_stations[st][0][s]

                if(min_of_sum < currsum):
                    min_of_sum = currsum
                    minel = st

            print(f"Для объекта {GetInfo(st)['name']}, id = {st} сумма кратчайших расстояний от него до всех домов минимальна")

        #Для какого объекта инфраструктуры построенное дерево кратчайших путей имеет минимальный вес
        if(args.sum_of_tree is not None):
            min_of_tree = float('inf')
            mintree = None
            for st in stations:
                tree = graph.GetTree(builds, res_stations[st][1])
                sumoftree = graph.GetSumOfTree(tree,G)
                if(min_of_tree < sumoftree):
                    min_of_tree = sumoftree
                    mintree = st

            print(f"Дерево кратчайших путей имеет минимальный вес для {GetInfo(st)['name']}, id = {st}")

        # Определить, какой из объектов расположен так, что расстояние между ним и самым дальним домом минимально
        if(args.mindist_fs is not None):
            mindist_global = float('inf')
            resfs = None
            for st in stations:
                # Ищем максимально удаленый дом
                maxdist = 0
                for s in res_stations[st][0]:
                    if maxdist < res_stations[st][0][s] and res_stations[st][0][s] != float('inf'):
                        maxdist = res_stations[st][0][s]
                if maxdist < mindist_global:
                    mindist_global = maxdist
                    resfs = st
            print(f"Объект {GetInfo(resfs)['name']} с id = {resfs} расположен так, что расстояние между ним и самым дальним домом минимально")

        # Для каждого дома определить объекты, расположенные не далее, чем в X км
        if(args.set_distance is not None):
            X = args.set_distance

            not_far_stations = {}
            for b in builds:
                not_far_stations[b] = []
                for st in stations:
                    if res_builds[b][0][st] <= X:
                        not_far_stations[b].append(st)
            for b in builds:
                if len(not_far_stations[b]) > 0:
                    print(f"Для дома {b} следующие станции находятся ближе чем в {X} условных км досигаемости(при движении от дома к станции): {not_far_stations[b]}")
                else:
                    print(f"Для дома {b} никакие станции не находятся ближе чем в {X} условных км досигаемости(при движении от дома к станции)")
            print("-----------------------------------------------------------------------------------------------------------")

            for b in builds:
                 not_far_stations[b] = []
                 for st in stations:
                    if res_stations[st][0][b] <= X:
                        not_far_stations[b].append(st)
            for b in builds:
                if len(not_far_stations[b]) > 0:
                    print(f"Для дома {b} следующие станции находятся ближе чем в {X} условных км досигаемости(при движении от станции к дому): {not_far_stations[b]}")
                else:
                    print(f"Для дома {b} никакие станции не находятся ближе чем в {X} условных км досигаемости(при движении от станции к дому)")
            print("-----------------------------------------------------------------------------------------------------------")

            for b in builds:
                 not_far_stations[b] = []
                 for st in stations:
                    if res_stations[st][0][b]+res_builds[b][0][st] <= X:
                        not_far_stations[b].append(st)
            for b in builds:
                if len(not_far_stations[b]) > 0:
                    print(f"Для дома {b} следующие станции находятся ближе чем в {X} условных км досигаемости(при необходимости возвращения): {not_far_stations[b]}")
                else:
                    print(f"Для дома {b} никакие станции не находятся ближе чем в {X} условных км досигаемости(при необходимости возвращения)")
    # Вторая часть Исследовательской работы. Кластеры--------------------------------------------------------------------------------------------
    if(args.data_for_clusters is not None):
        n = args.data_for_clusters[0]
        # Pick random n buildings and 1 firestation
        builds, station = GetBuildingsObjects(args.data_for_clusters[1],n ,1)

        # Lets build a tree
        station = station[0]
        dij = graph.DijkstraWithFinishNodes(G, station, builds)
        tree = graph.GetTree(builds, dij[1])

        # Тут наверно надо нарисовать дерево

        # Считаем длину дерева
        treelen = graph.GetSumOfTree(tree, G) # return sum of tree; edges - from GetTree, adj_list from GetGraphList

        # Считаем сумму кратчайших расстояний
        that_sum = 0
        for el in dij[0]:
            if(dij[0][el] != float('inf')):
                that_sum+= dij[0][el]

        print(f"Сумма кратчайших расстояний равна {that_sum}")


        res_builds = {}
        res_stations = {}
        mindist_from_builds = {}
        mindist_from_stations = {}

        #Сюда идет исследование для К = 2,3,4

        K = [2] #3,4]

        for k in K:
            clu = clusters.Get_k_Clusters(builds, G, k)

            # Поиск центроид
            print("начался поиск центроид")
            center = clusters.Find_Centers(clu, G)
            print("Центроиды: ",center)

            # Поиск кратчайших путей в кластерах
            pos = 0
            for c in clu:
                ccen = center[pos] # центроида этого кластера

                cdij =  graph.DijkstraWithFinishNodes(G, ccen, c)
                ctree = graph.GetTree(c, cdij[1])

                # Считаем длину дерева
                ctreelen = graph.GetSumOfTree(ctree, G)
                print(f"Для {pos}-го кластера длина дерева равна {ctreelen}")

                # Считаем сумму кратчайших расстояний
                csum = 0
                for el in cdij[0]:
                    if(cdij[0][el]!=float('inf')):
                        csum+= cdij[0][el]

                print(f"Сумма кратчайших расстояний для {pos}-го кластера равна {csum}")
                pos+=1
    # Построение Дендрограммы
    if(args.dendrogram is not None):
        n = args.dendrogram[0]
        # Pick random n buildings and 1 firestation
        builds, station = GetBuildingsObjects(args.dendrogram[0],n ,1)

        plt.figure()
        dn = hierarchy.dendrogram(clusters.Get_Dendro_matr(builds, G))
        plt.savefig('foo.pdf')

        #if(args.no_recalc_values is None):
         #   print("here we go")
    if(args.get_2_3_5_clusters is not None):
        n = args.get_2_3_5_clusters[0]
        # Pick random n buildings and 1 firestation
        builds, station = GetBuildingsObjects(args.get_2_3_5_clusters[1],n ,1)
        print(len(builds))
        print(station)
        print('-'*25)

        #res_5, res_3, res_2, dendromatr = clusters.Get_Clusters(builds, G)
        #Сюда идет исследование для К = 2,3,4

        K = [5]

        for k in K:
            print(k)
            clu = None
            if(k == 2):
                clu = sl.load_obj("res_2")
            else:
                clu = clusters.Get_k_Clusters(builds, G, k)
                sl.save_obj(clu, "res_"+str(k))

            # Поиск центроид
            print("начался поиск центроид")
            center = clusters.Find_Centers(clu, G)
            sl.save_obj(center,"center" + str(k))
            print("Центроиды: ",center)

            # Дерево кратчайших путей от станции до центроидов
            #fs_to_cen = sl.load_obj("fs_to_cen_"+str(k))
            fs_to_cen = graph.DijkstraWithFinishNodes(G, station[0], center)
            fs_to_cen_tree = graph.GetTree(center,fs_to_cen[1])
            #fs_to_cen_tree = sl.load_obj("fs_to_cen_tree_"+str(k))
            sl.save_obj(fs_to_cen, "fs_to_cen_"+str(k))
            sl.save_obj(fs_to_cen_tree, "fs_to_cen_tree_"+str(k))


            # Сумма кратчайших расстояний
            that_sum = 0
            for el in fs_to_cen[0]:
                if(fs_to_cen[0][el] != float('inf')):
                    that_sum+= fs_to_cen[0][el]

            print(f"Сумма кратчайших расстояний равна {that_sum}")
            # Поиск кратчайших путей в кластерах
            pos = 0
            for c in clu:
                ccen = center[pos] # центроида этого кластера

                cdij =  graph.DijkstraWithFinishNodes(G, ccen, c)
                sl.save_obj(cdij,"cdij"+str(k)+str(pos))
                ctree = graph.GetTree(c, cdij[1])
                sl.save_obj(ctree,"ctree"+str(k)+str(pos))

                # Считаем длину дерева
                ctreelen = graph.GetSumOfTree(ctree, G)

                print(f"Для {pos}-го кластера длина дерева равна {ctreelen}")



                # Считаем сумму кратчайших расстояний
                #csum = 0
                #for el in cdij[0]:
                 #   if(cdij[0][el]!=float('inf')):
                  #      csum+= cdij[0][el]


                  #print(f"Сумма кратчайших расстояний для {pos}-го кластера равна {csum}")
                pos+=1
        #sl.save_obj(res_5,"res_5")
        #sl.save_obj(res_3,"res_3")
        #sl.save_obj(res_2,"res_2")

        #sl.save_obj(dendromatr, "dendromatr")

    if(args.get_2_3_5_clusters_load is not None):
        n = args.get_2_3_5_clusters[0]
        # Pick random n buildings and 1 firestation
        builds, station = GetBuildingsObjects(args.get_2_3_5_clusters[1],n ,1)
        print(len(builds))
        print(station)
        print('-'*25)

        #res_5, res_3, res_2, dendromatr = clusters.Get_Clusters(builds, G)
        #Сюда идет исследование для К = 2,3,4

        K = [5]

        for k in K:
            print(k)
            clu = None
            if(k == 2):
                clu = sl.load_obj("res_2")
            else:
                clu = clusters.Get_k_Clusters(builds, G, k)
                sl.save_obj(clu, "res_"+str(k))

            # Поиск центроид
            print("начался поиск центроид")
            center = clusters.Find_Centers(clu, G)
            sl.save_obj(center,"center" + str(k))
            print("Центроиды: ",center)

            # Дерево кратчайших путей от станции до центроидов
            #fs_to_cen = sl.load_obj("fs_to_cen_"+str(k))
            fs_to_cen = graph.DijkstraWithFinishNodes(G, station[0], center)
            fs_to_cen_tree = graph.GetTree(center,fs_to_cen[1])
            #fs_to_cen_tree = sl.load_obj("fs_to_cen_tree_"+str(k))
            sl.save_obj(fs_to_cen, "fs_to_cen_"+str(k))
            sl.save_obj(fs_to_cen_tree, "fs_to_cen_tree_"+str(k))


            # Сумма кратчайших расстояний
            that_sum = 0
            for el in fs_to_cen[0]:
                if(fs_to_cen[0][el] != float('inf')):
                    that_sum+= fs_to_cen[0][el]

            print(f"Сумма кратчайших расстояний равна {that_sum}")
            # Поиск кратчайших путей в кластерах
            pos = 0
            for c in clu:
                ccen = center[pos] # центроида этого кластера

                cdij =  graph.DijkstraWithFinishNodes(G, ccen, c)
                sl.save_obj(cdij,"cdij"+str(k)+str(pos))
                ctree = graph.GetTree(c, cdij[1])
                sl.save_obj(ctree,"ctree"+str(k)+str(pos))

                # Считаем длину дерева
                ctreelen = graph.GetSumOfTree(ctree, G)

                print(f"Для {pos}-го кластера длина дерева равна {ctreelen}")



                # Считаем сумму кратчайших расстояний
                #csum = 0
                #for el in cdij[0]:
                 #   if(cdij[0][el]!=float('inf')):
                  #      csum+= cdij[0][el]


                  #print(f"Сумма кратчайших расстояний для {pos}-го кластера равна {csum}")
                pos+=1


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("-sf", "--show_fs", help="Show all firestations", action='store_true')
    #parser.add_argument("-sb", "--show_build", help="Show all buildings", action = 'store_true')
    parser.add_argument("-i", "--info", help="Get info by id", type = str)
    parser.add_argument("-pfb", "--pick_fs_and_bds", help="Write firestation number, than buildings number, than seed.", type = int, nargs=3)
    parser.add_argument("--sum_of_tree", help='Find firestation with lowest sum of tree of shortest paths', action='store_true', default = None)
    parser.add_argument("--sum_of_paths", help='Find firestation with lowest sum of shortest paths', action='store_true', default = None)
    parser.add_argument("--both_sides", help='Find min for both sides', action='store_true', default = None)
    parser.add_argument("--no_recalc_values", action = "store_true", default = None, help = "TODO")
    parser.add_argument("--mindist_fs", action = "store_true", default = None, help = "TODO")
    parser.add_argument("--set_distance", type = float, help = "TODO")

    # Clasters

    parser.add_argument("-dfc", "--data_for_clusters", help="Write buildings number, than seed.", type = int, nargs=2)
    parser.add_argument("-dg", "--dendrogram", help = "Write buildings number, than seed.", type = int, nargs = 2)
    parser.add_argument("-g235", "--get_2_3_5_clusters", help = "Get clusters for k = 2,3,5", type = int, nargs = 2)
    parser.add_argument("-g235l", "--get_2_3_5_clusters_load", help = "Get clusters for k = 2,3,5 with load", type = int, nargs = 2)

    args = parser.parse_args()

    main(args)
