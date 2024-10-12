import pandas as pd
import sys
import logging
import os


# Configure standard logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def summary_statistics(df):
    logger.info("Summary Statistics:")
    print("Summary Statistics:")
    summary_stats = df.describe()
    #summary_stats = self.df.describe(include='all')
    logger.info(f"\n{summary_stats}")
    print(f"\n{summary_stats}")
    return summary_stats

def missing_values(df):
    logger.info("Checking for missing values:")
    print("Checking for missing values:")
    missing_vals = df.isnull().sum()
    logger.info(f"\n{missing_vals}")
    print(f"\n{missing_vals}")
    return missing_vals

def data_types(df):
    logger.info("Checking data types:")
    print("Checking data types:")
    data_types = df.dtypes
    logger.info(f"\n{data_types}")
    print(f"\n{data_types}")
                         
def process_data(file_name):
    # Define the path to the '../data' folder
    data_folder_path = os.path.join(os.path.dirname(__file__), '../data')
    
    # Create the full path for the CSV file
    file_path = os.path.join(data_folder_path, file_name)

    # Log the absolute file path being accessed
    logging.info(f"Attempting to read file at: {os.path.abspath(file_path)}")

    # Load the DataFrame from the CSV file
    try:
        dataset = pd.read_csv(file_path)
        
        # Print out the first few rows
        print("Data from the CSV file:")
        print(dataset.head())

        data_types(dataset)
        missing_values(dataset)
        summary_statistics(dataset)

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
