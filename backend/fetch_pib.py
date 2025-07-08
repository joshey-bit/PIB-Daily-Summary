# Fetch PIB Daily Releases
# Scrape PIB, extract articles, call summarizer, save JSON

import requests
from bs4 import BeautifulSoup
import os
import json
from datetime import datetime

PIB_URL = "https://pib.gov.in/AllRel.aspx"
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

def fetch_pib_articles():
    """
    Scrape PIB All Releases page and extract articles (title, ministry, link, date, body).
    Returns a list of dicts.
    """
    resp = requests.get(PIB_URL)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')

    articles = []
    current_ministry = None
    today = datetime.now().date()

    # The structure is: Ministry headings (h3/h4), then links (a) for articles
    a_tags = soup.find_all('a')
    print(f"Found {len(a_tags)} <a> tags on the page.")
    print(f"Found {len(a_tags)} <a> tags on the page.")
    # Print all unique <a> hrefs containing 'PressReleasePage'
    pr_hrefs = set()
    for a in a_tags:
        href = a.get('href', '')
        if 'PressReleasePage' in href:
            pr_hrefs.add(href)
    print(f"Found {len(pr_hrefs)} unique press release hrefs:")
    for href in list(pr_hrefs)[:20]:
        print(href)
    # Print a few ministry headings for debug
    for h in soup.find_all(['h3', 'h4'])[:5]:
        print(f"Ministry heading: {h.get_text(strip=True)}")

    # ...existing code...
    for tag in soup.find_all(['h3', 'h4', 'a']):
        if tag.name in ['h3', 'h4']:
            current_ministry = tag.get_text(strip=True)
        elif tag.name == 'a' and tag.get('href', '').startswith('/PressReleasePage.aspx?PRID='):
            title = tag.get_text(strip=True)
            article_url = f"https://www.pib.gov.in{tag['href']}"
            date = str(today)
            body = fetch_article_body(article_url)
            articles.append({
                'title': title,
                'ministry': current_ministry or '',
                'date': date,
                'link': article_url,
                'body': body
            })
    return articles

def fetch_article_body(url):
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')
        # PIB article body is usually in this div
        content = soup.find('div', id='divContent')
        if content:
            return content.get_text(separator='\n', strip=True)
        return ""
    except Exception:
        return ""

def save_articles_json(articles, date=None):
    if not articles:
        return
    if not date:
        date = articles[0]['date']
    os.makedirs(DATA_DIR, exist_ok=True)
    out_path = os.path.join(DATA_DIR, f"{date}.json")
    # Format as per roadmap
    def extract_tags(title, ministry):
        tags = set()
        # Clean ministry name for tag
        abbr_map = {
            'mod': 'ministry of defence',
            'mha': 'ministry of home affairs',
            'mof': 'ministry of finance',
            'mhrd': 'ministry of education',
            'mohfw': 'ministry of health and family welfare',
            'morth': 'ministry of road transport and highways',
            'moc': 'ministry of coal',
            'moc&f': 'ministry of chemicals and fertilizers',
            'mofpi': 'ministry of food processing industries',
            'moefcc': 'ministry of environment, forest and climate change',
            'mea': 'ministry of external affairs',
            'meity': 'ministry of electronics and information technology',
            'mib': 'ministry of information and broadcasting',
            'mocw': 'ministry of communications',
            'mospi': 'ministry of statistics and programme implementation',
            'mpp': 'ministry of parliamentary affairs',
            'mnes': 'ministry of new and renewable energy',
            'moma': 'ministry of minority affairs',
            'mowr': 'ministry of water resources',
            'mohua': 'ministry of housing and urban affairs',
            'mota': 'ministry of tribal affairs',
            'mowcd': 'ministry of women and child development',
            'mocca': 'ministry of civil aviation',
            'mord': 'ministry of rural development',
            'msp': 'ministry of steel',
            'mmt': 'ministry of mines',
            'mha&fw': 'ministry of health and family welfare',
        }
        min_tag = None
        if ministry:
            min_tag = ministry.lower().replace('ministry of ', '').replace('&', 'and').replace(' ', '-').strip()
            tags.add(min_tag)
        # Detect abbreviations in title and add full form as tag
        title_lc = title.lower()
        for abbr, full in abbr_map.items():
            if abbr in title_lc or abbr.upper() in title or abbr.replace('&','and') in title_lc:
                tags.add(full)
        # Simple topic mapping for keywords in title
        topic_map = {
            'bank': 'banking',
            'finance': 'finance',
            'education': 'education',
            'school': 'education',
            'airport': 'infrastructure',
            'road': 'infrastructure',
            'rail': 'infrastructure',
            'startup': 'startup',
            'ai': 'technology',
            'solar': 'energy',
            'energy': 'energy',
            'plantation': 'environment',
            'environment': 'environment',
            'committee': 'governance',
            'policy': 'policy',
            'scheme': 'welfare',
            'drive': 'campaign',
            'application': 'process',
            'meeting': 'event',
            'launch': 'event',
            'initiative': 'event',
            'divas': 'event',
            'india': 'india',
        }
        for k, v in topic_map.items():
            if k in title_lc:
                tags.add(v)
        return list(tags)[:3]

    summaries = [
        {
            'title': a['title'],
            'ministry': a['ministry'],
            'summary': '',  # To be filled by summarizer
            'tags': extract_tags(a['title'], a['ministry'])
        } for a in articles
    ]
    data = {'date': date, 'summaries': summaries}
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(summaries)} articles to {out_path}")

if __name__ == "__main__":
    articles = fetch_pib_articles()
    if articles:
        save_articles_json(articles)
    else:
        print("No articles found.")
