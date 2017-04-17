import csv
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "-d", "--db-dir", required=True, help="Where traffic db is be stored")
parser.add_argument(
    "-o", "--output-dir", required=True, help="Where analysis output is be stored")
parser.add_argument(
    "-e", "--error-dir", required=True, help="Where regex error can be stored")
args = parser.parse_args()

conn = open(args.db_dir, 'r', newline='')
c = csv.reader(conn)

urls = {}
errors = []

count = 1

for row in c:
    url = row[2]
    if url == 'No match' or url == 'Hybrid Ad':
        errors.append([row[1], row[2], row[3]])
    if url.startswith("https://analytics.liftoff.io/v1/campaign_click?channel=doubleclick"):
        assert url[102] == '&'
        url = url[:102]
    elif url.startswith("https://apiservices.krxd.net/click_tracker/"):
        url = url.split("&clk=")[-1]
    if url in urls:
        urls[url].append(count)
    else:
        urls[url] = [count]
    count += 1

conn.close()

conn = open(args.output_dir, 'w', newline='')
c = csv.writer(conn)
for k in urls:
    c.writerow(
        [k, len(urls[k]), str(urls[k])[1:-1], sum(urls[k]) / len(urls[k])])
conn.close()

conn = open(args.error_dir, 'a', newline='')
c = csv.writer(conn)
for k in errors:
    c.writerow(k)
conn.close()
