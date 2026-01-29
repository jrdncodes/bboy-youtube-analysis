import os
import requests
import psycopg2
import html
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")
SEARCH_QUERY = os.getenv("SEARCH_QUERY", "bboy battle")

# --- DATABASE CONNECTION ---
conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
)
cur = conn.cursor()

# --- YOUTUBE SEARCH API ---
url = "https://www.googleapis.com/youtube/v3/search"

rows = []
next_page_token = None

while True:
    params = {
        "part": "snippet",
        "q": SEARCH_QUERY,
        "type": "video",
        "maxResults": 50,
        "pageToken": next_page_token,
        "key": API_KEY,
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    for item in data["items"]:
        rows.append(
            (
                item["id"]["videoId"],
                html.unescape(item["snippet"]["title"]),
                item["snippet"]["publishedAt"][:10],
                None,
            )
        )

    next_page_token = data.get("nextPageToken")
    if not next_page_token or len(rows) >= 200:
        break

# --- INSERT INTO POSTGRES ---
cur.executemany(
    """
    INSERT INTO public.videos (video_id, title, published_at, view_count)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (video_id) DO NOTHING
    """,
    rows,
)

conn.commit()
cur.close()
conn.close()

print(f"Inserted {len(rows)} rows")
