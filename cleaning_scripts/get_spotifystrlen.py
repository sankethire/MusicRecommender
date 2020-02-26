import csv

filename = "../csv/raw/songs/dataset-of-90s.csv"

fields = []
rows = []
with open(filename, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    fields = next(csvreader)
    for row in csvreader:
        rows.append(len(row[2]))

for r in rows:
    if(r!=36):
        print(False)

