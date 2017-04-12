import sqlite3
import re

conn = sqlite3.connect("/home/tonyyang/Desktop/ad_traffic_EN.db")

c = conn.cursor()

urls = set()
keys = set()

for row in c.execute('SELECT * FROM ad'):
    url = row[1]
    regex = re.compile('\w*=.{8}-.{4}-.{4}-.{4}-.{12}')
    match = regex.search(url)
    urls.add(match.group(0))

for k in urls:
    print(k)
