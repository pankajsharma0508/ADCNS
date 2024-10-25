import pandas as pd
import sys
import logging
import os

from prefect import get_run_logger
from sklearn.calibration import LabelEncoder


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


import pandas as pd

def bin_win_by_runs(df):
    # Update win_by_runs to None where win_by_wickets has a non-zero value
    
    filtered_df = df[df['win_by_runs'] > 0].copy()
    # Define updated bins for win_by_runs
    # Define bins and labels
    bins_runs = [0, 5, 15, 30, 50, 100, 151]  # Note: 151 is used to include 150 in the last bin
    labels_runs = ['0-5', '6-15', '16-30', '31-50', '51-100', '101-150']
    df['win_by_runs_bins'] = pd.cut(filtered_df['win_by_runs'], bins=bins_runs, labels=labels_runs, right=False)
    
    
    return df

def bin_win_by_wickets(df):
    # Define updated bins for win_by_wickets
    df['win_by_wickets'] = pd.to_numeric(df['win_by_wickets'], errors='coerce')
    filtered_df = df[df['win_by_wickets'] > 0].copy()
    
    bins_wickets =  [1, 3, 6, 11] # 4 edges for 3 labels
    labels_wickets = ['wkt(<2)', 'wkt(<3-5)', 'wkt(>6)']  # 3 labels
     # Create bins for win_by_wickets
    df['win_by_wickets_bins'] = pd.cut(filtered_df['win_by_wickets'], bins=bins_wickets, labels=labels_wickets, right=False)
    
    return df

def Perform_Binning(df):
    bin_win_by_runs(df)
    bin_win_by_wickets(df)

def clean_data(df):
        
        #logger.info("Cleaning up teams names from the dataset:")

        print("Cleaning up teams names from the dataset:")        
        team_counts = df['team1'].value_counts()

        # logger.info('IPL teams list ')
        # logger.info(team_counts)

        print('IPL teams list ')
        #print(team_counts)

        print('Replace values in team1 , team2 column Delhi Daredevils -> Delhi Capitals and Deccan Chargers -> Sunrisers Hyderabad')
        df['team1'] = df['team1'].replace('Delhi Daredevils', 'Delhi Capitals')
        df['team1'] = df['team1'].replace('Deccan Chargers', 'Sunrisers Hyderabad')

        # Replace values in 'team2' column
        df['team2'] = df['team2'].replace('Delhi Daredevils', 'Delhi Capitals')
        df['team2'] = df['team2'].replace('Deccan Chargers', 'Sunrisers Hyderabad')

           # Replace values in 'team2' column
        df['team1'] = df['team1'].replace('Rising Pune Supergiant', 'Rising Pune Supergiants')
        df['team2'] = df['team2'].replace('Rising Pune Supergiant', 'Rising Pune Supergiants')

        # Log the number of rows containing 'Deccan Chargers' in 'team1'
        deccan_rows = df.loc[df['team1'] == 'Deccan Chargers']
        #logger.info(f'Deccan Chargers Rows in team1: {deccan_rows.shape[0]}')

        # Log the number of rows containing 'Delhi Daredevils' in 'team1'
        d_rows = df.loc[df['team1'] == 'Delhi Daredevils']
        #logger.info(f'Delhi Daredevils Rows in team1: {d_rows.shape[0]}')

        team_counts = df['team1'].value_counts()
        print('IPL teams list after replacement')
        print(team_counts)
        #encode(df)
        print('Updating missing values in city  player of the match and winner and umpires columns')
        
        fill_values = {
            'city': 'Dubai',
            'umpire1': 'Aleem Dar',
            'umpire2': 'Aleem Dar',
            'umpire3': 'Aleem Dar',
            'player_of_match': 'N/A'
        }

        for column, value in fill_values.items():
          df.loc[:, column] = df[column].fillna(value)


        missing_vals = df.isnull().sum()
        print(f"\n checking again missing values{missing_vals}")

        print ("Performing Binning on win by run and win by wickets columns")
        Perform_Binning(df)
        print(df)
        remove_columns(df)
        print(df.dtypes)
        
        
def remove_columns(df):
     print('removing columns id, season,city,date, player_of_match, umpire1, umpire2,umpire3 ')
     df.drop(["id", "season","city","date", 'umpire1', "umpire2","umpire3"], axis=1, inplace=True)
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
