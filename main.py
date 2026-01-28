import requests
from bs4 import BeautifulSoup
import PyRSS2Gen
import datetime

url = "https://www.foodsecurityportal.org/news-and-blogs"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

items = []
# Find all article elements
for article in soup.find_all('article'):
    # Find the title link within h2.article-ref--title
    title_tag = article.find('h2', class_='article-ref--title')
    if title_tag:
        link_tag = title_tag.find('a')
        if link_tag:
            title = link_tag.text.strip()
            link = link_tag.get('href', '')
            
            # Make sure the link is absolute
            if link.startswith('/'):
                link = "https://www.foodsecurityportal.org" + link
            
            # Extract the excerpt/description if available
            excerpt_tag = article.find('div', class_='article-ref--excerpt')
            description = excerpt_tag.text.strip() if excerpt_tag else title
            
            # Extract the publication date if available
            date_tag = article.find('span', class_='article-ref--created')
            pub_date = datetime.datetime.now()
            if date_tag:
                try:
                    # Parse date like "Jan 15th, 2026"
                    date_str = date_tag.text.strip()
                    pub_date = datetime.datetime.strptime(date_str, "%b %dth, %Y")
                except:
                    try:
                        pub_date = datetime.datetime.strptime(date_str, "%b %dst, %Y")
                    except:
                        try:
                            pub_date = datetime.datetime.strptime(date_str, "%b %dnd, %Y")
                        except:
                            try:
                                pub_date = datetime.datetime.strptime(date_str, "%b %drd, %Y")
                            except:
                                pub_date = datetime.datetime.now()
            
            # Adding to the RSS list
            items.append(PyRSS2Gen.RSSItem(
                title = title,
                link = link,
                description = description,
                pubDate = pub_date
            ))

rss = PyRSS2Gen.RSS2(
    title = "Food Security Portal News & Blogs",
    link = url,
    description = "Latest updates from the Food Security Portal",
    lastBuildDate = datetime.datetime.now(),
    items = items
)

rss.write_xml(open("fsp_news_feed.xml", "w"))