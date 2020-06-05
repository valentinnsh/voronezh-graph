import pandas as pd
import graph
import csv
import test
import main
import saveload as sl
import numpy as np



df = pd.read_csv('export_test4.csv')
fc_list=list(df.iloc[:,0])
df = df.drop([df.columns[0]], axis=1)
df.to_csv('file_1.csv', index=False)
a_stream = open("file_1.csv", "r")

reader = csv.reader(a_stream)
next(reader)
data = list(reader)

#print(data)
#print(fc_list)
res = []
res.append(fc_list)
d = test.formGraphList(fc_list,data)
print('gas!gas!gas!')
f_list = [str(node) for node in fc_list]
for node in fc_list:
    row = []
    (D,Parent) = graph.Dijkstra(d,str(node))
    for i in range(len(fc_list)+1):
        if i == 0:
            row.append(node)
        else:
            row.append(int(D[str(i-1)]))
    res.append(row)
print(res)
myFile = open('test_4.csv', 'w', newline='')
with myFile:
    writer = csv.writer(myFile)
    writer.writerows(res)

'''
f_list = [str(node) for node in fc_list]

tree = graph.GetTree(f_list, Parent)
print("tree from b_id[0] (one of the objects) to a_id (sample of houses):")    
print(tree)
print("length of previous tree:")
print(graph.GetSumOfTree(tree,d))
'''
