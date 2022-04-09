import re
import time
import urllib3
import optparse
from urllib.parse import urljoin


parser = optparse.OptionParser()
parser.add_option("-t", "--target", dest="target", help="target domain")
(options, args) = parser.parse_args()

# checking if user has specified a target
if not options.target:
    print("[-] Please specify a target")
    exit(0)

terget = options.target
THREADS = 40

extracted_links = []


def link_extractor(terget):
    """
    This function odes the following;
    - scraps and extractcall links from the terget website to
    - does data cleaning to prepare the kink for futher user
    - stores all the links to a lists for futher processing

    """

    try:
        http = urllib3.PoolManager(
            num_pools=THREADS,
            maxsize=20,
            block=True,
        )
        r = http.request("GET", terget, retries=False)
        response = re.findall('(?:href=")(.*?)"', str(r.data))

        for link in response:
            if terget not in link:
                link = urljoin(terget, link)
                extracted_links.append(link)
            if "facebook" or "linkedin" or "twitter" or "instagram" in link:
                continue
            if link in extracted_links:
                continue

    except Exception as e:
        print(e)


link_extractor(terget)


def spider():
    """
    This function gets all the stored links and use them to scarp more links from the pages.
    - Cleans all the extracted links
    """
    tic = time.perf_counter()
    extracted_links_list = []
    for link in extracted_links:
        try:
            http = urllib3.PoolManager(
                num_pools=THREADS,
                maxsize=40,
                block=True,
                timeout=urllib3.Timeout(connect=3.0, read=120),
            )
            r = http.request("GET", link, retries=False)
            # extracting only links from the response
            response = re.findall('(?:href=")(.*?)"', str(r.data))

            for link in response:
                if terget not in link and not terget.startswith("http"):
                    link = str(terget) + str(link)
                    link = urljoin(terget, link)

                if link.startswith("#"):
                    continue
                print(link)

        except Exception as e:
            print(e)
        # if user presses Ctrl+C
        except KeyboardInterrupt:
            print("\n[-] Program Interrupted and Terminated")
            exit(0)
    toc = time.perf_counter()
    process_time = toc - tic
    print(
        "==============Spidering done==============\n in "
        + str(process_time)
        + " seconds"
    )


spider()
