import collections
import csv
import os

import requests

IN_FILE = "UK Accounts & Websites.csv"
OUT_FILE = "urls.csv"

# read the output file to know what we've attempted so far
done = set()
out = []
if os.path.exists(OUT_FILE):
    with open(OUT_FILE, "r") as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            done.add(row[0])
            out.append(row)

# load in the nput file and begin requesting the companies url
with open(IN_FILE, "r") as f:
    reader = csv.reader(f)
    for i, row in enumerate(reader):
        if i == 0:
            continue
        else:
            sfid = row[0]
            name = row[1]
            url = row[2]

            if url:
                try:
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
                        "Upgrade-Insecure-Requests": "1", "DNT": "1",
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                        "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate"}

                    if not url.startswith("http://"):
                        url = "http://" + url

                    print(f"{i}: {url}")

                    response = requests.get(url, timeout=10, headers=headers)

                    if response.history:
                        for resp in response.history:
                            print(f"\t{resp.status_code} - {resp.url}")
                        print(f"\t{response.status_code} - {response.url}")
                        row = row + [True, response.url]
                    else:
                        row = row + [False, response.url]
                except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout, requests.exceptions.TooManyRedirects, requests.exceptions.InvalidURL):
                    print("\tfailed")
                    row = row + [False, ]

            out.append(row)

        with open(OUT_FILE, "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerows(out)
