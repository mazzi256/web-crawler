import re
import time
import urllib3
import optparse
from urllib.parse import urljoin, urlparse, parse_qs
from time import process_time

parser = optparse.OptionParser()
parser.add_option("-t", "--target", dest="target", help="target domain")
(options, args) = parser.parse_args()

# checking if the user has provide a target
if not options.target:
    print("[-] Please specify a target")
    exit(0)

terget = options.target
THREADS = 10

extracted_links = []


def link_extractor(terget):

    try:
        http = urllib3.PoolManager(
            num_pools=THREADS,
            maxsize=20,
            block=True,
            timeout=urllib3.Timeout(connect=3.0, read=120),
        )
        r = http.request("GET", terget, retries=False)

    except Exception as e:
        print(e)
    return re.findall('(?:href=")(.*?)"', str(r.data))


def spider(terget):
    tic = time.perf_counter()
    extracted_links = link_extractor(terget)
    try:
        for link in extracted_links:
            link = str(terget) + str(link)
            if terget not in link:
                link = urllib3.parse.urljoin(terget, link)
                # urllib.parse.urljoin(url,link)
            striped = "#"
            if "#" in link or link.startswith("#"):
                link = link.replace(striped, "")

            extracted_links.append(link)
            if link not in extracted_links:
                # link.split("https")
                print(link)
                spider(link)

    except Exception as e:
        print(e)

    except KeyboardInterrupt:
        print("\n[-] Program Interrupted")
        exit(0)

    toc = time.perf_counter()

    print("==============Spidering done==============\n in " + tic - toc)


spider(terget)
