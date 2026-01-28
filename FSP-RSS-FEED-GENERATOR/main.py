import requests
from bs4 import BeautifulSoup
import PyRSS2Gen
import datetime

url = "https://www.foodsecurityportal.org/news-and-blogs"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

items = []
# The portal uses 'views-row' for the blog list items
for article in soup.find_all('div', class_='views-row'):
    title_tag = article.find('a')
    if title_tag:
        title = title_tag.text.strip()
        link = "https://www.foodsecurityportal.org" + title_tag['href']
        
        # Adding to the RSS list
        items.append(PyRSS2Gen.RSSItem(
            title = title,
            link = link,
            description = title, # Or extract the summary text
            pubDate = datetime.datetime.now()
        ))

rss = PyRSS2Gen.RSS2(
    title = "Food Security Portal News & Blogs",
    link = url,
    description = "Latest updates from the Food Security Portal",
    lastBuildDate = datetime.datetime.now(),
    items = items
)

rss.write_xml(open("fsp_news_feed.xml", "w"))