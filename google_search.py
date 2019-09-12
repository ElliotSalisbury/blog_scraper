import csv

from urllib.parse import urlparse
from url_normalize import url_normalize
from googlesearch import search

DATA_FILE = r"C:\Users\Elliot\PycharmProjects\emint\scraper\duedil\joined3.csv"

with open(DATA_FILE, "r") as f:
    reader = csv.reader(f)
    for i, row in enumerate(reader):
        if i == 0:
            continue

        if row[7] == "High - A":
            sfid = row[0]
            website = row[2]
            url_normed = url_normalize(website)
            url_hostname = urlparse(url_normed).hostname.replace("www.", "")

            print(f"{url_hostname}")
            query = f"site:{url_hostname} news"
            results = search(query=query, num=10,stop=10,pause=2)
            for r in results:
                print(f"\t{r}")
