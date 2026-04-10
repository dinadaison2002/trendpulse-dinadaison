import pandas as pd
import numpy as np
import os

def run_analysis():
    # --- Step 1: Load and Explore ---
    file_path = 'data/trends_clean.csv'
    
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found! Run Task 2 first.")
        return

    df = pd.read_json if file_path.endswith('.json') else pd.read_csv(file_path)
    df = pd.read_csv(file_path)

    print(f"Loaded data: {df.shape}")
    print("\nFirst 5 rows:")
    print(df.head())

    # Average score and comments using Pandas
    avg_score = df['score'].mean()
    avg_comments = df['num_comments'].mean()
    print(f"\nAverage score   : {avg_score:.2f}")
    print(f"Average comments: {avg_comments:.2f}")

    # --- Step 2: Basic Analysis with NumPy ---
    # Converting columns to NumPy arrays for calculation
    scores_array = df['score'].to_numpy()
    
    mean_score = np.mean(scores_array)
    median_score = np.median(scores_array)
    std_score = np.std(scores_array)
    max_score = np.max(scores_array)
    min_score = np.min(scores_array)

    print("\n--- NumPy Stats ---")
    print(f"Mean score   : {mean_score:.2f}")
    print(f"Median score : {median_score:.2f}")
    print(f"Std deviation: {std_score:.2f}")
    print(f"Max score    : {max_score}")
    print(f"Min score    : {min_score}")

    # Category with most stories (Pandas idxmax is easier here)
    top_category = df['category'].value_counts().idxmax()
    category_count = df['category'].value_counts().max()
    print(f"Most stories in: {top_category} ({category_count} stories)")

    # Story with most comments
    max_comments_idx = df['num_comments'].idxmax()
    top_story = df.loc[max_comments_idx]
    print(f"Most commented story: \"{top_story['title']}\" — {top_story['num_comments']} comments")

    # --- Step 3: Add New Columns ---
    # Formula: engagement = num_comments / (score + 1)
    df['engagement'] = df['num_comments'] / (df['score'] + 1)
    
    # is_popular: True if score > average score
    df['is_popular'] = df['score'] > avg_score

    # --- Step 4: Save the Result ---
    output_file = 'data/trends_analysed.csv'
    df.to_csv(output_file, index=False)
    
    print(f"\nSaved {len(df)} rows to {output_file}")
    print("Task 3 analysis complete!")

if __name__ == "__main__":
    run_analysis()