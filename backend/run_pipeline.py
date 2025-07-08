
import os
import json
from fetch_pib import fetch_pib_articles
from summarize import summarize_article

def run_pipeline():
    articles = fetch_pib_articles()
    if not articles:
        print("No articles found.")
        return
    summarized = []
    for a in articles:
        opt_title, summary = summarize_article(a['title'], a['body'], a['ministry'])
        # Recompute tags using the same logic as fetch_pib.py
        from fetch_pib import save_articles_json
        def extract_tags(title, ministry):
            tags = set()
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
            title_lc = title.lower()
            for abbr, full in abbr_map.items():
                if abbr in title_lc or abbr.upper() in title or abbr.replace('&','and') in title_lc:
                    tags.add(full)
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
        tags = extract_tags(opt_title, a['ministry'])
        summarized.append({
            'title': opt_title,
            'ministry': a['ministry'],
            'summary': summary,
            'tags': tags
        })
    # Save to JSON (use today's date)
    date = articles[0]['date']
    out_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{date}.json")
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump({'date': date, 'summaries': summarized}, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(summarized)} summarized articles to {out_path}")

if __name__ == "__main__":
    run_pipeline()
