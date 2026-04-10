import pandas as pd
import os
import glob

def process_data():
    # --- Step 1: Load the JSON File ---
    # Since the filename has a date, we use glob to find the latest trends_*.json
    json_files = glob.glob('data/trends_*.json')
    if not json_files:
        print("Error: No JSON data file found in data/ folder!")
        return

    # Picking the most recent file if multiple exist
    latest_file = max(json_files, key=os.path.getctime)
    
    df = pd.read_json(latest_file)
    print(f"Loaded {len(df)} stories from {latest_file}")

    # --- Step 2: Clean the Data ---
    
    # 1. Remove duplicates based on post_id
    df = df.drop_duplicates(subset=['post_id'])
    print(f"After removing duplicates: {len(df)}")

    # 2. Drop rows where essential fields (post_id, title, score) are missing
    df = df.dropna(subset=['post_id', 'title', 'score'])
    print(f"After removing nulls: {len(df)}")

    # 3. Data types - Ensure score and num_comments are integers
    # We use fillna(0) just in case num_comments was missing before conversion
    df['score'] = df['score'].astype(int)
    df['num_comments'] = df['num_comments'].fillna(0).astype(int)

    # 4. Low quality - Remove stories with score < 5
    df = df[df['score'] >= 5]
    print(f"After removing low scores: {len(df)}")

    # 5. Whitespace - Strip extra spaces from the title
    df['title'] = df['title'].str.strip()

    # --- Step 3: Save as CSV ---
    output_file = 'data/trends_clean.csv'
    df.to_csv(output_file, index=False)
    
    print(f"Saved {len(df)} rows to {output_file}")

    # Final Summary: Stories per category
    print("\nStories per category:")
    print(df['category'].value_counts())

if __name__ == "__main__":
    process_data()