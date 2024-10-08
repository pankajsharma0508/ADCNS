import logging
import pandas as pd

# Configure standard logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
class DataLoader:
    def __init__(self):
        #self.file_path = file_path
        logger.info(self.file_path)
        self.df = None

    def load_data(self):
        # Load the dataset
        self.df = pd.read_csv(self.file_path)
        logger.info("Dataset loaded successfully.")

        # Remove unwanted columns
        logger.info("Removing unwanted columns like umpire information")
        self.df.drop(['umpire2', 'umpire3', 'umpire1'], axis=1, inplace=True)

        # Remove records with no winner
        logger.info("Removing records which have no winner as they are not needed.")
        self.df = self.df.dropna(subset=['winner'])

        # Changing object types to string datatypes for relevant columns
        logger.info("Changing object types to string datatypes for string type columns")
        string_columns = ['city', 'team1', 'team2', 'toss_winner', 'toss_decision',
                          'winner', 'result', 'player_of_match', 'venue']
        self.df[string_columns] = self.df[string_columns].astype('string')

        # Convert 'date' column to datetime
        logger.info("Converting 'date' column to datetime format")
        self.df['date'] = pd.to_datetime(self.df['date'], errors='coerce')  # Handle invalid dates as NaT

        # Log DataFrame head
        logger.info(f"DataFrame head:\n{self.df.head()}")

        return self.df