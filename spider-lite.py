import re
import time
import urllib3
import optparse
import urllib.parse
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
THREADS = 50

extarcted_link_list = []

extracted_links_list = []


def spider(terget):
    print("spider stated...")
    tic = time.perf_counter()
    try:
        http = urllib3.PoolManager(
            num_pools=THREADS,
            maxsize=50,
            block=True,
            timeout=urllib3.Timeout(connect=3.0, read=120),
        )
        r = http.request("GET", terget, retries=False)
        extracted_links = re.findall('(?:href=")(.*?)"', str(r.data))

        for link in extracted_links:
            link = str(terget) + str(link)
            if terget not in link:
                link = urllib3.parse.urljoin(terget, link)
                # urllib.parse.urljoin(url,link)
            striped = "#"
            if "#" in link or link.startswith("#"):
                link = link.replace(striped, "")

            if link not in extracted_links_list:
                extracted_links_list.append(link)

                print(link)
            # if link not in extracted_links_list:
            #     # link.split("https")
            #     print(link)

    except Exception as e:
        print(e)

    except KeyboardInterrupt:
        print("\n[-] Program Interrupted")
        exit(0)

    toc = time.perf_counter()
    process_time = toc - tic

    print(
        "==============Spidering done==============\n in "
        + "========="
        + str(process_time)
        + "========="
    )


spider(terget)
