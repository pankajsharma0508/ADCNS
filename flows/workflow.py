from prefect import flow, task, get_run_logger
import subprocess
import os
import pandas as pd
import json  # Assuming the dataset will be in JSON format, adjust if needed
import tempfile
from prefect.artifacts import create_link_artifact
from io import StringIO

@task(log_prints=True)
def run_task(script_name):
    logger = get_run_logger()

    # Define the full path to the script based on the project structure
    script_path = os.path.join(os.path.dirname(__file__), '../tasks', script_name)

    try:
        # Run the external Python script using its full path
        result = subprocess.run(['python', script_path], capture_output=True, text=True)

        # Log both stdout and stderr
        if result.returncode == 0:
            logger.info(f"Successfully executed {script_name}:\n{result.stdout}")
            
            # Assuming the output is a JSON string containing the dataset
            # Convert the stdout to a Python object (e.g., list, dict)
            dataset = json.loads(result.stdout)
        else:
            logger.error(f"Error in {script_name}: {result.stderr}")
            return None

    except Exception as e:
        logger.error(f"Failed to execute {script_name}: {str(e)}")
        return None

    return dataset  # Return the dataset for further processing

from prefect import task, get_run_logger
import subprocess
import os
import pandas as pd

def save_to_file(dataset: pd.DataFrame, file_name: str):
    logger = get_run_logger()

    # Define the path to the '../data' folder
    data_folder_path = os.path.join(os.path.dirname(__file__), '../data')

    # Create the directory if it doesn't exist
    if not os.path.exists(data_folder_path):
        os.makedirs(data_folder_path)
        logger.info(f"Created folder: {data_folder_path}")

    # Define the full path for the CSV file
    csv_file_path = os.path.join(data_folder_path, file_name)

    # Save the DataFrame as a CSV in the '../data' folder
    dataset.to_csv(csv_file_path, index=False)
    logger.info(f"CSV file created: {csv_file_path}")
    return csv_file_path

@task(log_prints=True)
def run_task_with_csv(csv_file_path:str, script_name: str):
    logger = get_run_logger()    
    # Define the full path to the script
    script_path = os.path.join(os.path.dirname(__file__), '../tasks', script_name)

    try:
        # Pass the CSV file path to the external script via command line arguments
        logger.info(f"Running script {script_path} with data from {csv_file_path}")
        result = subprocess.run(['python', script_path, csv_file_path], capture_output=True, text=True)

        # Log both stdout and stderr
        if result.returncode == 0:
            logger.info(f"Successfully executed {script_name}:\n{result.stdout}")
        else:
            logger.error(f"Error in {script_name}: {result.stderr}")

    except Exception as e:
        logger.error(f"Failed to execute {script_name}: {str(e)}")

    return 0


@task(log_prints=True)
def preprocess_data(dataset):
    logger = get_run_logger()
    
    # Example preprocessing logic
    logger.info("Preprocessing data...")
    
    # For demo purposes, let's just log the first item or a sample
    #logger.info(f"First item of the dataset: {dataset.head()}")
    
    # You can implement additional preprocessing steps here
    # E.g., filtering, transformations, etc.
    
    return dataset  # Return preprocessed data if needed


@flow
def main_flow():
     
    create_link_artifact(
            key="irregular-data",
            link="https://www.kaggle.com/datasets/saurav9786/indian-premier-league-match-analysis",
            description="## This is a sample artifact ",
        )
    logger = get_run_logger()
    # Run the load_dataset task
    dataset = run_task("load_dataset.py")
    dataFrame = pd.read_json(StringIO(dataset), orient='records')
    if dataset is not None:
        # Pass the dataset to the preprocessing task        
        logger.info(f"Data loaded from csv !!")
        csv_file_path = save_to_file(dataFrame,"dataset.csv")    
        #pass the dataset to the task and run it in a subprocess 
        # # read the dataset and print basic stats on the data set
        run_task_with_csv(csv_file_path, "basic-stats.py")
        
        logger.info('Start data preprocessing converting columns to correct data types other tasks ....')
        run_task_with_csv(csv_file_path, "data-preprocessing.py")
        run_task("data-analysis.py")
        logger.info('starting  model traning ')
        run_task('train-model.py')

        logger.info("Connecting to prefect with REST API ");
        run_task('../api/deploymentAPI.py')
        run_task('../api/flowApi.py')
        run_task('../api/api.py')
        
        

       

# To run locally
if __name__ == "__main__":
    main_flow.serve(
        name="win-predictor-dataset",
        tags=["Indian Premier League - Win Predictor Application"],
        parameters={},
        interval=60
    )
