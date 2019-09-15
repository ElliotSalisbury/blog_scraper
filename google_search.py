import csv
import os

from urllib.parse import urlparse
from url_normalize import url_normalize
from googlesearch import search

URL_FILE = r".\urls.csv"
OUT_FILE = r".\news.csv"

done = set()
out = []
if os.path.exists(OUT_FILE):
    with open(OUT_FILE, "r") as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            done.add(row[0])
            out.append(row)

with open(URL_FILE, "r") as f:
    reader = csv.reader(f)
    for i, row in enumerate(reader):
        if row[0] in done:
            continue

        sfid = row[0]
        name = row[1]
        url = row[2]

        if len(row) == 6:
            url = row[5]

        try:
            url_normed = url_normalize(url)
            url_hostname = urlparse(url_normed).hostname.replace("www.", "")

            print(f"{url_hostname}")
            query = f"site:{url_hostname} news OR blog OR press"
            results = set(search(query=query, num=10,stop=10,pause=2))
            for r in results:
                out.append([sfid, r])
                print(f"\t{r}")
        except:
            out.append([sfid,])

        with open(OUT_FILE, "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerows(out)

