import time
import argparse
import urllib
import re
import sqlite3
try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    pass

p = None


class print_ad_dest:

    def __init__(self, db_dir):
        self.count = 0

        # primarily used for DataXu urls (https://i.w55c.net/*)
        self.regex1 = re.compile('rurl%3D(http|market).*?\\\\x26')

        # generic google redirects
        self.regex2 = re.compile('adurl=(http|market).*?\"')
        self.regex3 = re.compile(
            "adurl\\\\x3d(http|market).*?(?:\'|\"|\\\\x22)")

        self.conn = sqlite3.connect(db_dir)
        self.c = self.conn.cursor()

        print("Connected to db at " + db_dir)

        create_table = \
            "create table if not exists ad (method text, request_url text, ad_url text, response blob)"
        self.c.execute(create_table)
        self.conn.commit()

    def close(self):
        self.conn.close()

    def response(self, flow):
        try:
            if ("https://pubads.g.doubleclick.net/gampad/ads" in flow.request.pretty_url or
                    "https://googleads.g.doubleclick.net/mads/gma" in flow.request.pretty_url or
                    "https://ad.doubleclick.net/ddm/adj" in flow.request.pretty_url) \
                    and len(flow.response.content) > 0:
                print(
                    flow.request.method + " " + urllib.unquote(flow.request.pretty_url) + "\n")
                raw_html = flow.response.content

                ad_url = "No match"

                m1 = self.regex1.search(raw_html)
                m2 = self.regex2.search(raw_html)
                m3 = self.regex3.search(raw_html)
                if m1:
                    print(urllib.unquote(m1.group(0)[7:-4]) + '\n')
                    ad_url = urllib.unquote(m1.group(0)[7:-4])
                elif m2:
                    print(urllib.unquote(m2.group(0)[6:-1]) + '\n')
                    ad_url = urllib.unquote(m2.group(0)[6:-1])
                elif m3:
                    if m3.group(0)[-1] == "\'" or m3.group(0)[-1] == '\"':
                        print(urllib.unquote(m3.group(0)[9:-1]) + '\n')
                        ad_url = urllib.unquote(m3.group(0)[9:-1])
                    else:
                        print(urllib.unquote(m3.group(0)[9:-4]) + '\n')
                        ad_url = urllib.unquote(m3.group(0)[9:-4])
                else:
                    if "new HybridAds(" in raw_html:
                        print("Cannot support Hybrid Ads for now\n")
                        ad_url = "Hybrid Ad"
                    print("NO MATCH!!!!\n")
                try:
                    soup = BeautifulSoup(
                        raw_html.replace("\\x3d", "=").replace("\\x22", '"'))
                    raw_html = soup.prettify()
                except NameError:
                    pass
                self.c.execute(
                    """INSERT INTO ad VALUES (?, ?, ?, ?)""",
                    (flow.request.method,
                     urllib.unquote(flow.request.pretty_url),
                     ad_url,
                     buffer(raw_html)))
                self.conn.commit()
#                     with open("/tmp/" + str(self.count) + ".html.txt", "w") as f:
#                         f.write(
#                             "<!-- Original url: " + flow.request.pretty_url + " -->\n")
#                         try:
#                             soup = BeautifulSoup(
#                                 raw_html.replace("\\x3d", "=").replace("\\x22", '"'))
#                             f.write(soup.prettify())
#                         except NameError:
#                             f.write(raw_html)
                self.count += 1
            # else:
            #    print(flow.request.pretty_url)
        except KeyError:
            pass


def start():
    global p
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", "--db-dir", required=True, help="A directory in which traffic db can be stored")
    args = parser.parse_args()
    p = print_ad_dest(args.db_dir)
    return p


def done():
    p.close()
