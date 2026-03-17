import os
import requests
import psycopg2
import html
from dotenv import load_dotenv

# load environment variables
load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")
SEARCH_QUERY = os.getenv("SEARCH_QUERY", "bboy battle")

# Connect to dtabase
conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
)
cur = conn.cursor()

# Youtube Videos API
videos_url = "https://www.googleapis.com/youtube/v3/videos"
search_url = "https://www.googleapis.com/youtube/v3/search"


rows = []

def get_video_ids():
    video_ids = set()
    next_page_token = None

    date_ranges = [
        ("2023-01-01T00:00:00Z", "2023-12-31T23:59:59Z"),
        ("2024-01-01T00:00:00Z", "2024-12-31T23:59:59Z"),
        ("2025-01-01T00:00:00Z", "2025-12-31T23:59:59Z"),
    ]

    for start_date, end_date in date_ranges:
        print(f"--- Accessing Pivot: {start_date} to {end_date} ---")
        next_page_token = None

        while True:
            # Request parameters
            params = {
                "part": "snippet", # title,  date, thumbnail
                "q": SEARCH_QUERY,
                "type": "video",
                "maxResults": 50,
                "pageToken": next_page_token,
                "publishedAfter": start_date,  
                "publishedBefore": end_date,   
                "key": API_KEY,
            }

            # Error handling
            try:
                response = requests.get(search_url, params=params)
                response.raise_for_status()
                data = response.json()
            except requests.exceptions.HTTPError as e:
                # Check if it's specifically a Quota Error (403)
                if e.response.status_code == 403:
                    print("Quota Exceeded! Stopping search and processing what we have...")
                    return list(video_ids) # Exit function and return the set so far
                else:
                    print(f"An unexpected HTTP error occurred: {e}")
                    return list(video_ids) # Exit 

            # Loop through the videos
            for item in data["items"]:
                    video_ids.add(item["id"]["videoId"])
                    
            next_page_token = data.get("nextPageToken")
            print("Collected Video IDs:", len(video_ids))
            if not next_page_token or len(video_ids) >= 5000:
                break
    return list(video_ids)
    

def get_video_details(video_ids):
    rows = []

    for i in range(0, len(video_ids), 50):

        ids = ",".join(video_ids[i:i+50])

        params = {
            "part": "snippet,statistics",
            "id": ids,
            "key": API_KEY,
        }

        response = requests.get(videos_url, params=params)
        response.raise_for_status()
        data = response.json()

        for item in data["items"]:

            rows.append(
                (
                    item["id"],
                    html.unescape(item["snippet"]["title"]),
                    item["snippet"]["publishedAt"][:10],
                    int(item["statistics"].get("viewCount", 0)),
                    int(item["statistics"].get("likeCount", 0))
                )
            )

    return rows


def insert_rows(rows):
    # --- INSERT INTO POSTGRES ---
    cur.executemany(
        """
        INSERT INTO public.videos (video_id, title, published_at, view_count, like_count)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (video_id) DO NOTHING
        """,
        rows,
    )
    conn.commit()

video_ids = get_video_ids()

rows = get_video_details(video_ids)

insert_rows(rows)

cur.close()
conn.close()

print(f"Inserted {len(rows)} rows")