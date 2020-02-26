import csv

def listout(tags):
    tags = tags.split(";")
    tag_list = []
    for tag in tags:
        tag = tag.strip(" ")
        tag_list.append(tag)
    return tag_list

# s = "rap; urban; 90s; rnb; polish; slow jam; romantic ballads"
# print(listout(s))

filename = "artist_tags_clean.csv"

fields = []
rows = []
with open(filename, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    fields = next(csvreader)
    for row in csvreader:
        rows.append(row)

for r in rows:
    r[1] = listout(r[1])


new_rows = []
for r in rows:
    for s in r[1]:
        new_rows.append([r[0],s])



new_filename = "artist_tags_1nf_clean.csv"

with open(new_filename, 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fields)
    for r in new_rows:
        csvwriter.writerow(r)


