import pandas as pd
import sys
import logging
import os
import base64
import io
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
# Configure standard logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def train_model(df):
        # Dropping the target column and printing feature columns
        #print(df.describe)
        logger.info('Traning the model started ')
        #logger.info(df.describe)
        #print(df.columns)
        X = df.drop(["winner","venue"], axis=1)
        #X= df.drop(["city", "player_of_match", "venue"], axis=1, inplace=True)
        print(df.columns)        
        # Target variable
        y = df["winner"]

        logger.info('## Apply one-hot encoding on categorical variables')
        X = pd.get_dummies(X, ["team1","team2", "toss_winner", "toss_decision", "result"], drop_first = True)

        # # Encoding target labels
        le = LabelEncoder()
        y = le.fit_transform(y)

        # # Split data into train and test sets
        x_train, x_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=42)

        # # Initialize the model
        model = RandomForestClassifier(n_estimators=200, min_samples_split=3, max_features="sqrt")  # Updated max_features

        # # Fit the model on training data
        model.fit(x_train, y_train)

        # # Predict on the test data
        y_pred = model.predict(x_test)

        # # Calculate and print accuracy
        ac = accuracy_score(y_pred, y_test)
        print('Model Accuracy:', ac)


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
        print(f"Traning for model started from the CSV file: {file_path}")
        print(dataset.head())
        train_model(dataset)
       
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
