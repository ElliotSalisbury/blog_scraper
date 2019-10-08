import csv
import os

from usp.tree import sitemap_tree_for_homepage

URL_FILE = r".\urls.csv"
OUT_BLOG_FILE = r".\blogs.csv"
OUT_RSS_FILE = r".\rss.csv"

news_keywords = ["blog", "news", "press"]
rss_keywords = ["feed", "rss"]

done = set()
out_blog = []
out_rss = []
if os.path.exists(OUT_BLOG_FILE):
    with open(OUT_BLOG_FILE, "r", encoding='utf-8') as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            done.add(row[0])
            out_blog.append(row)
if os.path.exists(OUT_RSS_FILE):
    with open(OUT_RSS_FILE, "r", encoding='utf-8') as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            done.add(row[0])
            out_rss.append(row)


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

        url_hostname = url
        if not url_hostname.startswith("http"):
            url_hostname = "http://" + url_hostname


        tree = sitemap_tree_for_homepage(url_hostname)
        found_blog = False
        found_rss = False

        pages = set(tree.all_pages())
        if len(pages) > 0:
            for page in pages:
                purl = page.url

                if purl.endswith("/"):
                    purl = purl[:-1]

                if any(purl.endswith(x) for x in news_keywords):
                    out_blog.append([sfid, url_hostname, purl])
                    found_blog = True
                if any(purl.endswith(x) for x in rss_keywords):
                    out_rss.append([sfid, url_hostname, purl])
                    found_rss = True

        if not found_blog:
            out_blog.append([sfid, url_hostname])
        if not found_rss:
            out_rss.append([sfid, url_hostname])

        with open(OUT_BLOG_FILE, "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(out_blog)
        with open(OUT_RSS_FILE, "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(out_rss)
