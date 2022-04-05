#!/usr/bin/python3
# Path: crawler.py
import urllib3
import optparse
from time import process_time

parser = optparse.OptionParser()
parser.add_option("-t", "--target", dest="target", help="target domain")
(options, args) = parser.parse_args()

# checking if the user has provide a target
if not options.target:
    print("[-] Please specify a target")
    exit(0)

terget = str(options.target)
THREADS = 40


def request(terget):
    """
    This function does the following things:
    - Opens a file and reads all the subdomains to be added to the target domain eg mail.example.com
    - send GET requests to the target domain and subdomains to test if they exist
    """
    with open("test.txt", "r") as c:
        sub = c.read()

    for line in sub.split("\n"):
        start = process_time()  # calculate the time it takes to make a request

        try:
            http = urllib3.PoolManager(
                num_pools=THREADS,
                maxsize=50,
                block=True,
                timeout=urllib3.Timeout(connect=1.0, read=2.0),
            )

            r = http.request("GET", "https://" + line + "." + terget, retries=False)

            if r.status == 200:
                print(line + "." + terget)
            elif r.status == 404:
                pass

        except Exception as e:
            pass

        end = process_time()
    print(
        "--------------scan complete------------------- \n"
        + "----in "
        + str(end - start)
        + " seconds----"
    )


request(terget)
