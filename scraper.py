from scrapingbee import ScrapingBeeClient
from bs4 import BeautifulSoup
from datetime import datetime
import sqlite3, os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

client = ScrapingBeeClient(api_key=API_KEY)
DB_FILE = "database.db"

def scrape_and_store(url, data_type, selector, scrape_name):
    # 1. Fetch page using ScrapingBee library
    response = client.get(
        url,
        params={
            "render_js": "true"  # only if site uses JavaScript
        }
    )

    print('HTTP status code:', response.status_code)
    # response.content is bytes, decode to string
    html = response.content.decode("utf-8")  

    # 2. Parse HTML with BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")

    # 3. Extract elements
    if selector:
        elements = soup.select(selector)
    else:
        if data_type == "text":
            # default for quotes.toscrape.com
            if soup.select(".quote .text"):
                elements = soup.select(".quote .text")
            else:
                elements = soup.find_all(text=True)
        elif data_type == "links":
            elements = soup.find_all("a")
        elif data_type == "images":
            elements = soup.find_all("img")
        elif data_type == "table":
            elements = soup.find_all("table")
        else:
            elements = []

    # 4. Convert elements to strings
    data = []
    for e in elements:
        if hasattr(e, 'get_text'):
            text = e.get_text(strip=True)
            if text:
                data.append(text)
        elif e.name == "img" and e.has_attr("src"):
            data.append(e["src"])
        elif isinstance(e, str):
            text = e.strip()
            if text:
                data.append(text)

    if not data:
        data.append("No data found.")

    # 5. Store in SQLite
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(f"""CREATE TABLE IF NOT EXISTS "{scrape_name}" (
                 id INTEGER PRIMARY KEY,
                 content TEXT,
                 scraped_at DATETIME
                 )""")
    for item in data:
        c.execute(f"INSERT INTO '{scrape_name}' (content, scraped_at) VALUES (?, ?)", (item, datetime.now()))
    conn.commit()
    conn.close()

    return data[:10]  # return first 10 results