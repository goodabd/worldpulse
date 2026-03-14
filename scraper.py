import feedparser, json, os, datetime, requests
from google.generativeai import configure, GenerativeModel
configure(api_key=os.getenv('GEMINI_API_KEY'))
model = GenerativeModel('gemini-1.5-flash')

def fetch_rss(media, url):
    feed = feedparser.parse(url)
    items = []
    for e in feed.entries[:50]:
        items.append({"media": media, "title": e.title, "url": e.link, "publish_time": datetime.datetime.now().isoformat()})
    return items

# 数据采集
all_news = fetch_rss("NYT", "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml")
# 简化示例：实际可在此扩充列表
prompt = f"分析以下新闻，输出JSON数组(event_id, title, summary, category, importance_score): {json.dumps(all_news)}"
try:
    resp = model.generate_content(prompt)
    data = json.loads(resp.text.replace('```json','').replace('```',''))
    with open("data/news.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
except Exception as e:
    print(f"Error: {e}")
