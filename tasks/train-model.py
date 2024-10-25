import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import logging
import joblib  # To save the model
import seaborn as sns
import matplotlib.pyplot as plt

# Configure logger
logger = logging.getLogger(__name__)

# Shared Data Preprocessing Function
def preprocess_data(df):
    """Preprocesses the data by applying one-hot encoding and label encoding."""
    
    X = df.drop(["winner", "venue"], axis=1)
    y = df["winner"]

    # One-hot encoding for categorical variables
    X = pd.get_dummies(X, columns=["team1", "team2", "toss_winner", "toss_decision", "result","player_of_match"], drop_first=True)

    # Label encoding for the target variable
    le = LabelEncoder()
    y = le.fit_transform(y)

    return X, y, le  # Return LabelEncoder for later use

# Function to evaluate a model and return metrics
def evaluate_model(y_test, y_pred, model_name, model, label_encoder):
    """Evaluates the model on several metrics and prints the results."""
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted', zero_division=1)
    recall = recall_score(y_test, y_pred, average='weighted', zero_division=1)
    f1 = f1_score(y_test, y_pred, average='weighted', zero_division=1)
    cm = confusion_matrix(y_test, y_pred)

    # Get the class labels from the label encoder
    class_labels = label_encoder.classes_
    print (class_labels)

    logger.info(f'{model_name} Results:')
    logger.info(f'Accuracy: {accuracy:.4f}')
    logger.info(f'Precision: {precision:.4f}')
    logger.info(f'Recall: {recall:.4f}')
    logger.info(f'F1-Score: {f1:.4f}')
    
    print(f"{model_name} Metrics:")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1-Score: {f1:.4f}")
    
    # Plotting the confusion matrix with actual class labels
    # plt.figure(figsize=(6, 4))
    # sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=class_labels, yticklabels=class_labels)
    # plt.title(f'{model_name} - Confusion Matrix')
    # plt.xlabel('Predicted')
    # plt.ylabel('True')
    # plt.tight_layout()
    # plt.savefig(f"./output/{model_name}_confusion_matrix.png")
    #plt.show()
    
    return accuracy, precision, recall, f1

# Function for training Random Forest
def train_random_forest(X_train, X_test, y_train, y_test, label_encoder):
    logger.info('Training RandomForestClassifier')
    model = RandomForestClassifier(n_estimators=200, min_samples_split=3, max_features="sqrt")
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    #joblib.dump(model, "./output/random_forest_model.pkl")
    return evaluate_model(y_test, y_pred, "Random Forest", model=model, label_encoder=label_encoder)

# Function for training Logistic Regression
def train_logistic_regression(X_train, X_test, y_train, y_test, label_encoder):
    logger.info('Training LogisticRegression')
    model = LogisticRegression(max_iter=200)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    #joblib.dump(model, "./output/logistic_regression_model.pkl")
    return evaluate_model(y_test, y_pred, "Logistic Regression", model=model, label_encoder=label_encoder)

# Function for training K-Nearest Neighbors
def train_knn(X_train, X_test, y_train, y_test, label_encoder):
    logger.info('Training KNeighborsClassifier')
    model = KNeighborsClassifier(n_neighbors=5)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    #joblib.dump(model, "./output/knn_model.pkl")
    return evaluate_model(y_test, y_pred, "K-Nearest Neighbors", model=model, label_encoder=label_encoder)

# Function to compare different algorithms
def compare_algorithms(df):
    logger.info('Preprocessing the data')
    X, y, label_encoder = preprocess_data(df)

    # Split the data into train and test sets
    logger.info('Splitting data into training and testing sets')
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=42)

    # Train and evaluate different models
    logger.info('Comparing models')

    print("\nRandom Forest:")
    rf_metrics = train_random_forest(X_train, X_test, y_train, y_test, label_encoder)
    
    print("\nLogistic Regression:")
    lr_metrics = train_logistic_regression(X_train, X_test, y_train, y_test, label_encoder)
    
    print("\nK-Nearest Neighbors:")
    knn_metrics = train_knn(X_train, X_test, y_train, y_test, label_encoder)

    # Print the results in a comparison format
    print("\nModel Comparison (Accuracy, Precision, Recall, F1-Score):")
    print(f"Random Forest:        {rf_metrics}")
    print(f"Logistic Regression:  {lr_metrics}")
    print(f"K-Nearest Neighbors:  {knn_metrics}")

# Main function
def process_data_and_train(file_name):
    print(f"Reading dataset from {file_name}")
    # Define the path to the '../data' folder
    data_folder_path = os.path.join(os.path.dirname(__file__), '../data')
    
    # Create the full path for the CSV file
    file_path = os.path.join(data_folder_path, file_name)
    print(f"Reading dataset from {file_path}")

    # Load the dataset
    try:
        df = pd.read_csv(file_path)
        print(f"Dataset loaded successfully: {df.shape} rows, {df.shape[1]} columns")
        
        #encode(df)
        # Compare algorithms
        compare_algorithms(df)
    
    except Exception as e:
        logger.error(f"Error processing file: {e}")
        print(f"Error processing file: {e}")

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    print('Starting script...')

    # Call the function to process data and train models
    process_data_and_train("dataset_pre.csv")
