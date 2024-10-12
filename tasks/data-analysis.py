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
