import sqlite3

conn = sqlite3.connect("/home/tonyyang/Desktop/ad_traffic_EN.db")

c = conn.cursor()

urls = {}

for row in c.execute('SELECT * FROM ad'):
    url = row[2]
    if url in urls:
        urls[url] += 1
    else:
        urls[url] = 1
for k in urls:
    print(k)
