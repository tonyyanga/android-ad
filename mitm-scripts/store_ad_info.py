import time
import argparse
import urllib
import re
import sys
import csv
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
        self.regex2 = re.compile('adurl(=|%3D)(http|market).*?\"')
        self.regex3 = re.compile(
            "adurl\\\\x3d(http|market).*?(?:\'|\"|\\\\x22)")
        self.regex4 = re.compile('adurl=(http|market).*?\\n')
        self.regex5 = re.compile(
            '<IFRAME src=\"https://googleads.g.doubleclick.net/xbbe/pixel?')
        self.regex6 = re.compile(
            "<script src=\'https://a2.adformdsp.net/adfscript/")
        self.regex7 = re.compile(
            "<SCRIPT language=\'JavaScript1.1\' SRC=\"https://ad.doubleclick.net/ddm/adj/")

        self.conn = open(db_dir, 'w', newline='')
        self.c = csv.writer(self.conn)

        print("Connected to db at " + db_dir)

        # create_table = \
        #    "create table if not exists ad (method text, request_url text, ad_url text, response blob)"
        # self.c.execute(create_table)
        # self.conn.commit()

    def close(self):
        self.conn.close()

    def response(self, flow):
        try:
            if ("https://pubads.g.doubleclick.net/gampad/ad" in flow.request.pretty_url or
                    "https://googleads.g.doubleclick.net/mads/gma" in flow.request.pretty_url or
                    "https://ad.doubleclick.net/ddm/adj" in flow.request.pretty_url or
                    "https://googleads.g.doubleclick.net/xbbe/pixel?" in flow.request.pretty_url or
                    "https://a2.adformdsp.net/adfscript/" in flow.request.pretty_url or
                    "https://ad.doubleclick.net/ddm/adj/" in flow.request.pretty_url) \
                    and len(flow.response.content) > 0:
                # print(
                # flow.request.method + " " +
                # urllib.parse.unquote(flow.request.pretty_url) + "\n")
                raw_html = flow.response.content.decode('utf-8')

                ad_url = "No match"

                def m1():
                    return self.regex1.search(raw_html)

                def m2():
                    return self.regex2.search(raw_html)

                def m3():
                    return self.regex3.search(raw_html)

                def m4():
                    return self.regex4.search(raw_html)

                def ignore():
                    return self.regex5.search(raw_html) or self.regex6.search(raw_html) or self.regex7.search(raw_html)

                if m1():
                    #    print(urllib.parse.unquote(m1.group(0)[7:-4]) + '\n')
                    ad_url = urllib.parse.unquote(m1().group(0)[7:-4])
                elif m2():
                    #    print(urllib.parse.unquote(m2.group(0)[6:-1]) + '\n')
                    ad_url = urllib.parse.unquote(m2().group(0)[6:-1])
                    if ad_url[-1] == '\\':
                        ad_url = ad_url[:-1]
                elif m3():
                    if m3().group(0)[-1] == "\'" or m3().group(0)[-1] == '\"':
                        #        print(urllib.parse.unquote(m3.group(0)[9:-1]) + '\n')
                        ad_url = urllib.parse.unquote(m3().group(0)[9:-1])
                    else:
                        #        print(urllib.parse.unquote(m3.group(0)[9:-4]) + '\n')
                        ad_url = urllib.parse.unquote(m3().group(0)[9:-4])
                elif m4():
                    ad_url = urllib.parse.unquote(m4().group(0)[6:-1])
                elif ignore():
                    return
                else:
                    if "new HybridAds(" in raw_html:
                        #        print("Cannot support Hybrid Ads for now\n")
                        ad_url = "Hybrid Ad"
                    print("NO MATCH!!!!\n")
                try:
                    soup = BeautifulSoup(
                        raw_html.replace("\\x3d", "=").replace("\\x22", '"'))
                    raw_html = soup.prettify()
                except NameError:
                    pass
                self.c.writerow(
                    [flow.request.method,
                     urllib.parse.unquote(flow.request.pretty_url),
                     ad_url,
                     raw_html])
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
        "-d", "--db-dir", required=True, help="where traffic db can be stored")
    args = parser.parse_args()
    p = print_ad_dest(args.db_dir)
    return p


def done():
    p.close()
