import requests

websites = ["https://talkbackproductions.tv/news/",
            "https://www.cazenovecapital.com/media-centre/newsroom/",
            "https://www.cineworldplc.com/en/investors/press-releases/press-release",
            "https://www.connectgroupplc.com/press-centre",
            "https://www.criver.com/insights",
            "https://www.designbridge.com/blog/",
            "https://www.designbridge.com/category/blog/news/",
            "https://www.gerald.com/",
            "https://www.ibblaw.co.uk/insights/blog",
            "https://www.ibblaw.co.uk/insights/press-coverage",
            "https://www.im.natixis.com/uk/latest-insights",
            "https://www.neopost.com/newsroom/press-releases",
            "https://www.perkins.com/en_GB/company/news/corporate-press-release.html",
            "https://www.prsformusic.com/press",
            "https://www.redcentricplc.com/news-events/",
            "https://www.rics.org/uk/news-insight/latest-news/?search=&topics=&locations=&sort=3&contentTypes=",
            "https://www.torque.eu/news/",
            "https://www.tss.trelleborg.com/en/news-and-events/news/?sortType=&startItem=0&numberOfItems=10&id=080488f7-b871-41c0-b01e-1e4eed8ffca"]

for i, url in enumerate(websites):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
        "Upgrade-Insecure-Requests": "1", "DNT": "1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate"}
    response = requests.get(url, timeout=10, headers=headers)

    with open(f"new/{i}_web.html", "wb") as f:
        f.write(response.content)