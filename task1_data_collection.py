import requests
import json
import time
import os
from datetime import datetime
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Category Setup
categories_config = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "globals"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

# Session setup with Retries to avoid SSL EOF
session = requests.Session()
retries = Retry(total=3, backoff_factor=1, status_forcelist=[502, 503, 504])
session.mount('https://', HTTPAdapter(max_retries=retries))

headers = {"User-Agent": "TrendPulse/1.0"}

# stage - 2
def collect_trends():
    top_ids_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    
    try:
        # Increase timeout to 15 to handle slow connections
        response = session.get(top_ids_url, headers=headers, timeout=15)
        story_ids = response.json()[:500]
    except Exception as e:
        print(f"Initial API error: {e}")
        return []

    all_collected_stories = []
    category_counts = {cat: 0 for cat in categories_config}

    print("Starting data collection...")

    for cat_name, keywords in categories_config.items():
        print(f"Collecting for category: {cat_name}...")
        
        for s_id in story_ids:
            if category_counts[cat_name] >= 25:
                break

            try:
                item_url = f"https://hacker-news.firebaseio.com/v0/item/{s_id}.json"
                # Using session instead of direct requests
                item_res = session.get(item_url, headers=headers, timeout=10)
                
                if item_res.status_code != 200:
                    continue

                story = item_res.json()
                if not story or "title" not in story:
                    continue

                title = story.get("title", "").lower()

                if any(word in title for word in keywords):
                    story_data = {
                        "post_id": story.get("id"),
                        "title": story.get("title"),
                        "category": cat_name,
                        "score": story.get("score"),
                        "num_comments": story.get("descendants", 0),
                        "author": story.get("by"),
                        "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    all_collected_stories.append(story_data)
                    category_counts[cat_name] += 1
            
            except Exception:
                # Intha error vantha ippo crash aagathu, silent-ah skip pannum
                continue 

        print(f"Found {category_counts[cat_name]} stories for {cat_name}.")
        time.sleep(2) # Task instruction requirement

    return all_collected_stories

# stage - 3
def save_data(stories):
    if not os.path.exists('data'):
        os.makedirs('data')

    date_str = datetime.now().strftime("%Y%m%d")
    filename = f"data/trends_{date_str}.json"

    with open(filename, 'w') as f:
        json.dump(stories, f, indent=4)

    print(f"\n--- SUCCESS ---")
    print(f"Collected {len(stories)} stories total.")
    print(f"Saved to {filename}")

if __name__ == "__main__":
    data = collect_trends()
    save_data(data)