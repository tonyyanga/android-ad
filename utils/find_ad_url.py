import csv
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "-d", "--db-dir", required=True, help="Where traffic db is be stored")
parser.add_argument(
    "-s", "--segment", required=True, help="A segment of the target url")
args = parser.parse_args()

conn = open(args.db_dir, 'r', newline='')
c = csv.reader(conn)

count = 1

for row in c:
    url = row[2]
    if args.segment in url:
        print(url)
        conn.close()
        sys.exit(0)

conn.close()