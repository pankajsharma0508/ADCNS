import pandas as pd
import sys
import logging
import os

from prefect import get_run_logger


# Configure standard logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)
def save_to_file(dataset: pd.DataFrame, file_name: str):
   
    #print(f"CSV file created: {dataset.head()}")
    # Define the path to the '../data' folder
    data_folder_path = os.path.join(os.path.dirname(__file__), '../data')

    # Create the directory if it doesn't exist
    if not os.path.exists(data_folder_path):
        os.makedirs(data_folder_path)
        #logger.info(f"Created folder: {data_folder_path}")

    # Define the full path for the CSV file
    csv_file_path = os.path.join(data_folder_path, file_name)

    # Save the DataFrame as a CSV in the '../data' folder
    dataset.to_csv(csv_file_path, index=False)
    #logger.info(f"CSV file created: {csv_file_path}")
    print(f"CSV file created: {csv_file_path}")
    return csv_file_path

def clean_data(df):
        
        #logger.info("Cleaning up teams names from the dataset:")

        print("Cleaning up teams names from the dataset:")        
        team_counts = df['team1'].value_counts()

        # logger.info('IPL teams list ')
        # logger.info(team_counts)

        print('IPL teams list ')
        print(team_counts)

        print('Replace values in team1 , team2 column Delhi Daredevils -> Delhi Capitals and Deccan Chargers -> Sunrisers Hyderabad')
        df['team1'] = df['team1'].replace('Delhi Daredevils', 'Delhi Capitals')
        df['team1'] = df['team1'].replace('Deccan Chargers', 'Sunrisers Hyderabad')

        # Replace values in 'team2' column
        df['team2'] = df['team2'].replace('Delhi Daredevils', 'Delhi Capitals')
        df['team2'] = df['team2'].replace('Deccan Chargers', 'Sunrisers Hyderabad')

        # Log the number of rows containing 'Deccan Chargers' in 'team1'
        deccan_rows = df.loc[df['team1'] == 'Deccan Chargers']
        #logger.info(f'Deccan Chargers Rows in team1: {deccan_rows.shape[0]}')

        # Log the number of rows containing 'Delhi Daredevils' in 'team1'
        d_rows = df.loc[df['team1'] == 'Delhi Daredevils']
        #logger.info(f'Delhi Daredevils Rows in team1: {d_rows.shape[0]}')

        team_counts = df['team1'].value_counts()
        print('IPL teams list after replacement')
        print(team_counts)
        remove_columns(df)
       
        
def remove_columns(df):
     print('removing columns id, season,city,date, player_of_match, umpire1, umpire2,umpire3 ')
     df.drop(["id", "season","city","date", "player_of_match", 'umpire1', "umpire2","umpire3"], axis=1, inplace=True)
     print('after remove')
     save_to_file(df,'dataset_pre.csv')
     return df


def process_data(file_name):
    # Define the path to the '../data' folder
    data_folder_path = os.path.join(os.path.dirname(__file__), '../data')
    
    # Create the full path for the CSV file
    file_path = os.path.join(data_folder_path, file_name)

    # Log the absolute file path being accessed
    #logging.info(f"Attempting to read file at: {os.path.abspath(file_path)}")

    # Load the DataFrame from the CSV file
    try:
        dataset = pd.read_csv(file_path)
        
        # Print out the first few rows
        print("Data preprocessing started from the CSV file:")
        print(dataset.head())
        clean_data(dataset)

      

    except FileNotFoundError:
        logging.error(f"Error: The file '{file_path}' was not found.")
    except pd.errors.EmptyDataError:
        logging.error(f"Error: The file '{file_path}' is empty.")
    except pd.errors.ParserError:
        logging.error(f"Error: Could not parse the file '{file_path}'.")
    except Exception as e:
        logging.error(f"An error occurred while processing the file: {e}")

if __name__ == "__main__":
    print('Starting script...')  # Indicate the script has started
    logger.info('Getting the file name from command line arguments')
    
    if len(sys.argv) != 2:
        print("Usage: python DataLoader.py <file_name>")
        sys.exit(1)
    
    file_name = sys.argv[1]
    print(f"File name provided: {file_name}")
    
    # Call the function to process the data
    process_data(file_name)
