import csv
import collections
import operator

filename = "../csv/clean/artist_tags_1nf_clean.csv"

fields = []
rows = []
with open(filename, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    fields = next(csvreader)
    for row in csvreader:
        rows.append(row)


threshold = 3
thresh_artist_tags = []

csv_tagsfreq = "../csv/clean/tags_freq.csv"
fields_csv_tagsfreq = []
rows_csv_tagsfreq = {}
with open(csv_tagsfreq, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    fields_csv_tagsfreq = next(csvreader)
    for row in csvreader:
        if(int(row[2]) <= threshold ):
            rows_csv_tagsfreq[(row[1])] = 1

print(rows_csv_tagsfreq)


new_filename = "../csv/clean/frequent_artist_tags.csv"
with open(new_filename, 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fields)
    for r in rows:
        if not r[1] in rows_csv_tagsfreq:
            csvwriter.writerow(r)
