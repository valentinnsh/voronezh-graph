import xmlparser
import graph
import saveload
import matplotlib.pyplot as plt

def draw_city_graph(name):
    #node_coords = xmlparser.getNodesCoords().values()
    node_coords = saveload.load_obj("coords")

    #G = graph.GetGraphList()
    #save.save_obj(G, 'adj_list')
    G = saveload.load_obj(name)
    #node_coords = {'1':('1','1'),'2':('2','1'),'2.5':('2.5','2'),'3':('3','1'),'4':('4','0')}
    #G = {'1' : [('2','1'),('2.5','1')], '2.5': [('1','1'),('4','1'),('3','1')], '3':[('2.5','1'),('4','1')], '4':[('2.5','1'),('3','1')]}
    x = []
    y = []
    #x = [1,2,1,2.5,4,2.5,3,2.5,3,4]
    #y = [1,1,1,2,0,2,1,2,1,0]

    buildings = saveload.load_obj("buildings")
    bid = [ building['id'] for building in buildings]

    firestations = saveload.load_obj("firestations")
    fid = [ firestation['id'] for firestation in firestations]
    colors = []

    fig = plt.gcf()
    fig.set_size_inches(50, 50, forward=True)


    pos = 0
    total = len(G.keys())

   # with open('lens.txt', "w") as f:
    #    for i in G.keys():
     #       f.write("len(G[i] = " + str(len(G[i])) + '\n')

    for i in G.keys():
        if len(G[i]) > 4:
            print("len(", i, ") > 4 and equal ", len(G[i]))
    for i in G.keys():
        i_coords = (float(node_coords[i][0]),float(node_coords[i][1]))

        print("step ", pos, "from", total)
        pos += 1
        print(len(G[i]))
        for j in G[i]:
            j_coords = (float(node_coords[j[0]][0]),float(node_coords[j[0]][1]))
            x.append(float(i_coords[0])); x.append(float(j_coords[0]))
            y.append(float(i_coords[1])); y.append(float(j_coords[1]))
            if i in fid:
                colors.append("red")
            elif i in bid:
                colors.append("blue")
            else:
                colors.append("black")

            if j[0] in fid:
                colors.append("red")
            elif j[0] in bid:
                colors.append("blue")
            else:
                colors.append("black")

            plt.scatter(x[pos-1],y[pos-1],linewidths=10,c = colors[pos-1])
            plt.scatter(x[pos],y[pos],linewidths=10,c = colors[pos])
            plt.plot((x[pos-1], x[pos]), (y[pos-1], y[pos]), '-k')

    #for i in node_coords:
     #   print(i)
      #  x.append(float(i[0]))
       # y.append(float(i[    colors = []

    #for i in range(len(x)):
     #   plt.scatter(x[i],y[i],linewidths=10,c = colors[i])

    #for i in range(0,(len(x)-1),2):
     #   plt.plot((x[i], x[i+1]), (y[i], y[i+1]), '-k')
    #i = 0

    #for node in G:
     #   (node_lat, node_lon) = coords[node]
      #  node_lat = float(node_lat)
       # node_lon = float(node_lon)
        #for adj_node in G[node]:
         #   (adj_node_lat,adj_node_lon) = coords[adj_node]
          #  adj_node_lat = float(adj_node_lat)
           # adj_node_lon = float(adj_node_lon)
            #plt.plot([node_lat,adj_node_lat], [node_lon,adj_node_lon], 'black')
        #i = i + 1
        #print(i)
    fig.savefig('classic_Voronezh.png', dpi=100)

def draw_city_graph_rebrand(name):
    #node_coords = xmlparser.getNodesCoords().values()
    node_coords = saveload.load_obj("coords")


    #G = graph.GetGraphList()
    #saveload.save_obj(G, 'adj_list')
    G = saveload.load_obj(name)
    #node_coords = {'1':('1','1'),'2':('2','1'),'2.5':('2.5','2'),'3':('3','1'),'4':('4','0')}
    #G = {'1' : [('2','1'),('2.5','1')], '2.5': [('1','1'),('4','1'),('3','1')], '3':[('2.5','1'),('4','1')], '4':[('2.5','1'),('3','1')]}
    x = []
    y = []
    #x = [1,2,1,2.5,4,2.5,3,2.5,3,4]
    #y = [1,1,1,2,0,2,1,2,1,0]
    plt.ioff()

    buildings = saveload.load_obj("buildings")
    bid = [ building['id'] for building in buildings]

    firestations = saveload.load_obj("firestations")
    fid = [ firestation['id'] for firestation in firestations]
    colors = []

    fig = plt.gcf()
    fig.set_size_inches(50, 50, forward=True)


    pos = 0
    total = len(G.keys())

   # with open('lens.txt', "w") as f:
    #    for i in G.keys():
     #       f.write("len(G[i] = " + str(len(G[i])) + '\n')

    for i in G.keys():
        if len(G[i]) > 4:
            print("len(", i, ") > 4 and equal ", len(G[i]))

    for i in G.keys():
        i_coords = (float(node_coords[i][0]),float(node_coords[i][1]))

        print("step ", pos, "from", total)
        pos += 1
        print(len(G[i]))
        for j in G[i]:
            j_coords = (float(node_coords[j[0]][0]),float(node_coords[j[0]][1]))

            plt.scatter(float(i_coords[0]),float(i_coords[1]),linewidths=10,c = "blue")
            plt.scatter(float(j_coords[0]),float(j_coords[1]),linewidths=10,c = "blue")
            plt.plot((float(i_coords[0]), float(j_coords[0])), (float(i_coords[1]), float(j_coords[1])), '-k')


    #for i in node_coords:
     #   print(i)
      #  x.append(float(i[0]))
       # y.append(float(i[    colors = []

    #for i in range(len(x)):
     #   plt.scatter(x[i],y[i],linewidths=10,c = colors[i])

    #for i in range(0,(len(x)-1),2):
     #   plt.plot((x[i], x[i+1]), (y[i], y[i+1]), '-k')
    #i = 0

    #for node in G:
     #   (node_lat, node_lon) = coords[node]
      #  node_lat = float(node_lat)
       # node_lon = float(node_lon)
        #for adj_node in G[node]:
         #   (adj_node_lat,adj_node_lon) = coords[adj_node]
          #  adj_node_lat = float(adj_node_lat)
           # adj_node_lon = float(adj_node_lon)
            #plt.plot([node_lat,adj_node_lat], [node_lon,adj_node_lon], 'black')
        #i = i + 1
        #print(i)

    fig.savefig('classic_Voronezh.png', dpi=100)
    saveload.save_obj(fig, 'fig_demo')


def redraw_current():
    fig = saveload.load_obj('fig_demo')
    fig.set_size_inches(100, 100, forward=True)
    fig.savefig('classic_Voronezh_2.png', dpi=100)


def draw_tree(tree, name):
    fig = saveload.load_obj('fig_demo')
    fig.set_size_inches(100, 100, forward=True)
    node_coords = saveload.load_obj("coords")

    for e in tree:
        a = e[0]
        b = e[1]

        a_coords = (float(node_coords[e[0]][0]),float(node_coords[e[0]][1]))
        b_coords = (float(node_coords[e[1]][0]),float(node_coords[e[1]][1]))
        plt.plot((float(a_coords[0]), float(b_coords[0])), (float(a_coords[1]), float(b_coords[1])), '-r')
   fig.savefig(name, dpi = 100)

def draw_clusters_with_centers(clu, cen, name):
    fig = saveload.load_obj('fig_demo')
    fig.set_size_inches(100, 100, forward=True)
    node_coords = saveload.load_obj("coords")

    for c in clu:
        for v in c:
            v_coords = (float(node_coords[v][0]),float(node_coords[v][1]))
            plt.scatter(float(v_coords[0]),float(v_coords[1]),linewidths=20,c = "black")
    for v in cen:
        v_coords = (float(node_coords[v][0]),float(node_coords[v][1]))
        plt.scatter(float(v_coords[0]),float(v_coords[1]),linewidths=20,c = "red")

    fig.savefig(name, dpi = 100)



#redraw_current()
#draw_city_graph_rebrand('adj_list_47')
