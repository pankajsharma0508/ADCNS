import json
import logging
import pandas as pd

# Configure standard logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
def load_dataset():
    
    # Simulate loading a dataset (replace with actual logic)
    dataset = pd.read_csv("./data/matches.csv")
    logger.info("Dataset loaded successfully.")
    # Convert the DataFrame to a JSON string
    dataset_json = dataset.to_json(orient="records")
    # Output the dataset as JSON
    print(json.dumps(dataset_json))

def load_dataset1():
    # Simulate loading a dataset (replace with actual logic)
    dataset = [{"team": "Team A", "score": 200}, {"team": "Team B", "score": 150}]
    
   
    # Output the dataset as JSON
    print(json.dumps(dataset))

if __name__ == "__main__":
    load_dataset()
