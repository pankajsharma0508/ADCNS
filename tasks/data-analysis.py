import pandas as pd
import sys
import logging
import os
import base64
import io
import matplotlib.pyplot as plt
import seaborn as sns
import json

# Configure standard logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def create_output_folder():
    output_folder = "./output"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        logger.info(f"Created output folder: {output_folder}")
    return output_folder

def plot_matches_per_team(df):
    teams = pd.concat([df['team1'], df['team2']])
    team_counts = teams.value_counts()

    plt.figure(figsize=(10, 6))
    sns.barplot(x=team_counts.index, y=team_counts.values, palette="viridis")
    plt.title('Number of Matches Played by Each Team')
    plt.xlabel('Teams')
    plt.ylabel('Number of Matches')
    plt.xticks(rotation=90)
    plt.tight_layout()

    output_folder = create_output_folder()
    file_path = os.path.join(output_folder, 'plot_matches_per_team.png')
    plt.savefig(file_path)
    logger.info(f"Plot saved as {file_path}")

def plot_match_per_venue(df):
    plt.figure(figsize=(10, 6))
    sns.countplot(y='venue', data=df, order=df['venue'].value_counts().iloc[:10].index)
    plt.xlabel('No of matches', fontsize=12)
    plt.ylabel('Venue', fontsize=12)
    plt.title('Total Number of matches played in different stadium')
    plt.tight_layout()

    output_folder = create_output_folder()
    file_path = os.path.join(output_folder, 'plot_matches_per_venue.png')
    plt.savefig(file_path)
    logger.info(f"Plot saved as {file_path}")

def toss_winner(df):
    plt.figure(figsize=(10, 6))
    sns.countplot( x = 'toss_winner', data = df)
    plt.xticks(rotation='vertical')
   
    plt.xlabel('Teams', fontsize=12)
    plt.ylabel('Count of Toss', fontsize=12)
    plt.title('Total Number of toss winner')
    plt.tight_layout()

    output_folder = create_output_folder()
    file_path = os.path.join(output_folder, 'toss_winner.png')
    plt.savefig(file_path)
    logger.info(f"Plot saved as {file_path}")
def plot_pie_win_by_wickets(df):
    plt.figure(figsize=(8, 8))
    win_by_wickets_counts = df['win_by_wickets_bins'].value_counts()
    plt.pie(win_by_wickets_counts, labels=win_by_wickets_counts.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('plasma', len(win_by_wickets_counts)))
    plt.title('Distribution of Wins by Wickets')
    plt.axis('equal')
    output_folder = create_output_folder()
    file_path = os.path.join(output_folder, 'plot_pie_win_by_wickets.png')
    plt.savefig(file_path)
    logger.info(f"Plot saved as {file_path}")

def plot_pie_win_by_runs(df):
    plt.figure(figsize=(8, 8))
    win_by_runs_counts = df['win_by_runs_bins'].value_counts()
    plt.pie(win_by_runs_counts, labels=win_by_runs_counts.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('viridis', len(win_by_runs_counts)))
    plt.title('Distribution of Wins by Runs')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    output_folder = create_output_folder()
    file_path = os.path.join(output_folder, 'plot_pie_win_by_runs.png')
    plt.savefig(file_path)
    logger.info(f"Plot saved as {file_path}")




def best_Player(df):
    top_players = df.player_of_match.value_counts()[:10]
    #sns.barplot(x="day", y="total_bill", data=tips)
    fig, ax = plt.subplots()
    ax.set_ylim([0,20])
    ax.set_ylabel("Number of Awards")
    ax.set_xlabel("Name of Players")
    ax.set_title("Top player of the match Winners")
    #top_players.plot.bar()
    sns.barplot(x = top_players.index, y = top_players, orient='v', palette="RdBu");
    plt.xticks(rotation = 'vertical')
    output_folder = create_output_folder()
    file_path = os.path.join(output_folder, 'top_player.png')
    plt.savefig(file_path)
    logger.info(f"Plot saved as {file_path}")

def process_data(file_name):
    # Define the path to the '../data' folder
    data_folder_path = os.path.join(os.path.dirname(__file__), '../data')
    
    # Create the full path for the CSV file
    file_path = os.path.join(data_folder_path, file_name)

    # Log the absolute file path being accessed
    logger.info(f"Attempting to read file at: {os.path.abspath(file_path)}")

    # Load the DataFrame from the CSV file
    try:
        dataset = pd.read_csv(file_path)
        
        # Print out the first few rows
        print(f"Data analysis started from the CSV file: {file_path}")
        print(dataset.head())
        
        # Call plotting functions
        plot_matches_per_team(dataset)
        plot_match_per_venue(dataset)
        toss_winner(dataset)
        best_Player(dataset)
        plot_pie_win_by_runs(dataset)
        plot_pie_win_by_wickets(dataset)
         # Convert the DataFrame to a JSON string
        #dataset_json = dataset.to_json(orient="records")
        # Output the dataset as JSON
        #print(json.dumps(dataset_json))

    except FileNotFoundError:
        logger.error(f"Error: The file '{file_path}' was not found.")
    except pd.errors.EmptyDataError:
        logger.error(f"Error: The file '{file_path}' is empty.")
    except pd.errors.ParserError:
        logger.error(f"Error: Could not parse the file '{file_path}'.")
    except Exception as e:
        logger.error(f"An error occurred while processing the file: {e}")

if __name__ == "__main__":
    print('Starting script...')  # Indicate the script has started
    
    # Uncomment the following lines if you want to pass file name as argument
    # if len(sys.argv) != 2:
    #     print("Usage: python DataLoader.py <file_name>")
    #     sys.exit(1)
    # file_name = sys.argv[1]
    
    # For now, hardcoding the file name
    process_data("dataset_pre.csv")
