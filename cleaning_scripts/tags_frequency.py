import csv
import collections
import operator

filename = "../csv/clean/artist_tags_1nf_clean.csv"

fields = []
tags = []
with open(filename, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    fields = next(csvreader)
    for row in csvreader:
        tags.append(row[1])

tags_frequency = dict(collections.Counter(tags))
tags_frequency = dict(sorted(tags_frequency.items(),key=operator.itemgetter(1),reverse=True))

new_filename = "../csv/clean/tags_freq.csv"

threshold = 3
# print(type(tags_frequency))

tagfields = ['tag_id' ,'tags', 'frequency']
with open(new_filename, 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(tagfields)
    tagid = 1
    for r in tags_frequency:
        if(tags_frequency[r] > threshold):
            csvwriter.writerow([tagid,r,tags_frequency[r]])
            tagid += 1



