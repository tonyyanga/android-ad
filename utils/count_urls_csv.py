import csv

conn = open(
    "/home/tonyyang/Desktop/comparison experiment/comparison_treated.csv", 'r', newline='')

c = csv.reader(conn)

urls = {}

for row in c:
    url = row[2]
    if url in urls:
        urls[url] += 1
    else:
        urls[url] = 1
for k in urls:
    print(k)
