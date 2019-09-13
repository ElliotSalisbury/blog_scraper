import collections
import csv
import os
from urllib.parse import urlparse
from requests_futures.sessions import FuturesSession

import requests
from url_normalize import url_normalize

IN_FILE = "UK Accounts & Websites.csv"
OUT_FILE = "urls.csv"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    "Upgrade-Insecure-Requests": "1", "DNT": "1",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate"}
OUT_EVERY = 50

# read the output file to know what we've attempted so far
done = set()
out = []
if os.path.exists(OUT_FILE):
    with open(OUT_FILE, "r") as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            done.add(row[0])
            out.append(row)

# read the input file to know what we need to scrape next
todo = {}
# load in the nput file and begin requesting the companies url
with open(IN_FILE, "r") as f:
    reader = csv.reader(f)
    for i, row in enumerate(reader):
        if i == 0 or row[0] in done:
            continue
        else:
            todo[row[0]] = row

curr_out_size = len(out)

session = FuturesSession()

futures = {}
for k, row in todo.items():
    sfid = row[0]
    name = row[1]
    url = row[2]

    if url:
        url_normed = url
        try:
            url_normed = url_normalize(url)
            url_hostname = urlparse(url_normed).hostname.replace("www.", "")
            row[2] = url_hostname

            if not url_hostname.startswith("http://"):
                url_hostname = "http://" + url_hostname
            future = session.get(url_hostname, timeout=10, headers=headers)
            futures[sfid] = future
        except:
            pass

finished = False
while not finished:
    completed = {k:f for k, f in futures.items() if f.done()}
    [futures.pop(k) for k in completed]

    for sfid, future in completed.items():
        row = todo[sfid]
        try:
            print(f"({len(futures)}) {row[2]}")
            response = future.result()

            redirected = False
            if response.history:
                redirected = True
                for resp in response.history:
                    print(f"\t{resp.status_code} - {resp.url}")
                print(f"\t{response.status_code} - {response.url}")

            same_host = True
            if redirected:
                orig_url_hostname = row[2]
                new_url_normed = url_normalize(response.url)
                new_url_hostname = urlparse(new_url_normed).hostname.replace("www.", "")

                if orig_url_hostname != new_url_hostname:
                    same_host = False

                print(f"\tSame Hostname: {same_host}")

            row = row + [redirected, same_host, response.url]
        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout, requests.exceptions.TooManyRedirects, requests.exceptions.InvalidURL):
            print("\tfailed")
            row = row + [False,]
        out.append(row)

    if len(out) > curr_out_size + OUT_EVERY or len(futures) == 0:
        with open(OUT_FILE, "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerows(out)
        curr_out_size = len(out)

    if len(futures) == 0:
        finished = True