import pandas as pd
import graph
import csv
import test
df = pd.read_csv('export_test.csv')
fc_list=list(df.iloc[:,0])
df = df.drop([df.columns[0]], axis=1)
df.to_csv('file_1.csv', index=False)
a_stream = open("file_1.csv", "r")

reader = csv.reader(a_stream)
next(reader)
data = list(reader)

print(data)
print(fc_list)
d = test.formGraphList(fc_list,data)
print('gas!gas!gas!')
(D,Parent) = graph.Dijkstra(d,'0')
f_list = [str(node) for node in fc_list]
f_list.remove('0')
tree = graph.GetTree(f_list, Parent)
print("tree from b_id[0] (one of the objects) to a_id (sample of houses):")    
print(tree)
print("length of previous tree:")
print(graph.GetSumOfTree(tree,d))