import pandas as pd
import csv
import test
df = pd.read_csv('export_test2.csv')
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
print(d)