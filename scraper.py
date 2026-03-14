import feedparser, json, os, datetime, requests
from google.generativeai import configure, GenerativeModel

configure(api_key=os.getenv('GEMINI_API_KEY'))
model = GenerativeModel('gemini-1.5-flash')

# 媒体源配置
NEWS_RSS = ["https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml", "https://feeds.content.dowjones.io/public/rss/RSSWorldNews.xml"]
X_ACCOUNTS = ["nytimes", "WSJ", "washingtonpost", "Reuters"] # 可在此处增加您的18个账号

def get_news():
    all_items = []
    # 抓取 RSS
    for url in NEWS_RSS:
        feed = feedparser.parse(url)
        for e in feed.entries[:10]:
            all_items.append({"title": e.title, "summary": e.description[:200], "url": e.link})
    # 抓取社交媒体 (通过 Nitter)
    for user in X_ACCOUNTS:
        feed = feedparser.parse(f"https://nitter.net/{user}/rss")
        for e in feed.entries[:5]:
            all_items.append({"title": e.title, "summary": e.description[:200], "url": e.link})
    return all_items

data = get_news()
# AI 处理逻辑
prompt = f"分析以下新闻列表，生成JSON格式(包含title, summary, url)，不要任何Markdown符号: {json.dumps(data)}"
resp = model.generate_content(prompt)
final_data = json.loads(resp.text)

os.makedirs('data', exist_ok=True)
with open("data/news.json", "w", encoding="utf-8") as f:
    json.dump(final_data, f, ensure_ascii=False, indent=2)
