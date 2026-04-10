import pandas as pd
import matplotlib.pyplot as plt
import os

def create_visualizations():
    # --- Step 1: Setup ---
    file_path = 'data/trends_analysed.csv'
    if not os.path.exists(file_path):
        print("Error: trends_analysed.csv not found!")
        return

    df = pd.read_csv(file_path)
    
    # Create outputs folder if it doesn't exist
    if not os.path.exists('outputs'):
        os.makedirs('outputs')

    # --- Step 2: Chart 1 - Top 10 Stories by Score ---
    plt.figure(figsize=(10, 6))
    top_10 = df.nlargest(10, 'score').copy()
    
    # Shorten titles longer than 50 chars
    top_10['short_title'] = top_10['title'].apply(lambda x: x[:47] + "..." if len(x) > 50 else x)
    
    plt.barh(top_10['short_title'], top_10['score'], color='skyblue')
    plt.xlabel('Score')
    plt.ylabel('Story Title')
    plt.title('Top 10 Stories by Score')
    plt.gca().invert_yaxis()  # Highest score on top
    plt.tight_layout()
    plt.savefig('outputs/chart1_top_stories.png')
    plt.close()

    # --- Step 3: Chart 2 - Stories per Category ---
    plt.figure(figsize=(10, 6))
    cat_counts = df['category'].value_counts()
    colors = ['red', 'blue', 'green', 'orange', 'purple']
    
    cat_counts.plot(kind='bar', color=colors[:len(cat_counts)])
    plt.title('Number of Stories per Category')
    plt.xlabel('Category')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('outputs/chart2_categories.png')
    plt.close()

    # --- Step 4: Chart 3 - Score vs Comments ---
    plt.figure(figsize=(10, 6))
    popular = df[df['is_popular'] == True]
    not_popular = df[df['is_popular'] == False]
    
    plt.scatter(not_popular['score'], not_popular['num_comments'], color='gray', label='Non-Popular', alpha=0.5)
    plt.scatter(popular['score'], popular['num_comments'], color='gold', label='Popular', edgecolor='black')
    
    plt.title('Score vs Number of Comments')
    plt.xlabel('Score')
    plt.ylabel('Number of Comments')
    plt.legend()
    plt.tight_layout()
    plt.savefig('outputs/chart3_scatter.png')
    plt.close()

    # --- Bonus: Dashboard ---
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('TrendPulse Dashboard', fontsize=20)

    # Re-plot 1: Top 10
    axes[0, 0].barh(top_10['short_title'], top_10['score'], color='skyblue')
    axes[0, 0].set_title('Top 10 Stories')
    axes[0, 0].invert_yaxis()

    # Re-plot 2: Categories
    cat_counts.plot(kind='bar', color=colors[:len(cat_counts)], ax=axes[0, 1])
    axes[0, 1].set_title('Category Distribution')

    # Re-plot 3: Scatter
    axes[1, 0].scatter(not_popular['score'], not_popular['num_comments'], color='gray', alpha=0.5)
    axes[1, 0].scatter(popular['score'], popular['num_comments'], color='gold', edgecolor='black')
    axes[1, 0].set_title('Score vs Comments')
    
    # Hide the 4th empty subplot
    axes[1, 1].axis('off')
    axes[1, 1].text(0.1, 0.5, 'Pipeline Complete!\n- Fetch\n- Clean\n- Analyse\n- Visualise', fontsize=14)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig('outputs/dashboard.png')
    plt.close()

    print("Task 4 Complete! Charts saved in 'outputs/' folder.")

if __name__ == "__main__":
    create_visualizations()