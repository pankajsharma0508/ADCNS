import base64
import io
import logging
import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# Add the parent directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#from tasks import DataAnalyzer,DataLoader,cleandata

# Configure standard logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

class DataLoader:
    def __init__(self, file_path):
        self.file_path = file_path
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
    
    
class DataAnalyzer:
    def __init__(self, df):
        self.df = df

    def summary_statistics(self):
        logger.info("Summary Statistics:")
        summary_stats = self.df.describe()
        #summary_stats = self.df.describe(include='all')
        logger.info(f"\n{summary_stats}")
        return summary_stats

    def missing_values(self):
        logger.info("Checking for missing values:")
        missing_vals = self.df.isnull().sum()
        logger.info(f"\n{missing_vals}")
        return missing_vals

    def data_types(self):
        logger.info("Checking data types:")
        data_types = self.df.dtypes
        logger.info(f"\n{data_types}")
        return data_types
    
    def clean_data(self):
        logger.info("Cleaning up teams names from the dataset:")
        team = self.df.describe(include='all')
        team_counts = self.df['team1'].value_counts()
        logger.info('IPL teams list ')
        logger.info(team_counts)
        # Replace values in 'team1' column
        self.df['team1'] = self.df['team1'].replace('Delhi Daredevils', 'Delhi Capitals')
        self.df['team1'] = self.df['team1'].replace('Deccan Chargers', 'Sunrisers Hyderabad')

        # Replace values in 'team2' column
        self.df['team2'] = self.df['team2'].replace('Delhi Daredevils', 'Delhi Capitals')
        self.df['team2'] = self.df['team2'].replace('Deccan Chargers', 'Sunrisers Hyderabad')

        # Log the number of rows containing 'Deccan Chargers' in 'team1'
        deccan_rows = self.df.loc[self.df['team1'] == 'Deccan Chargers']
        #logger.info(f'Deccan Chargers Rows in team1: {deccan_rows.shape[0]}')

        # Log the number of rows containing 'Delhi Daredevils' in 'team1'
        d_rows = self.df.loc[self.df['team1'] == 'Delhi Daredevils']
        #logger.info(f'Delhi Daredevils Rows in team1: {d_rows.shape[0]}')

        team_counts = self.df['team1'].value_counts()
        logger.info('IPL teams list after replacement')
        logger.info(team_counts)
        

        #logger.info(f"\n replaced team names  ")
        #team_counts = self.df.value_counts()
        #logger.info(team_counts)

    def plot_matches_per_team(self):
        #        Function to plot the number of matches played by each team (combined from team1 and team2 columns).
         # Combine team1 and team2 into a single Series to count occurrences
        teams = pd.concat([self.df['team1'], self.df['team2']])

        # Count the occurrences of each team
        team_counts = teams.value_counts()

        # Plotting the bar graph using Seaborn
        plt.figure(figsize=(10, 6))
        sns.barplot(x=team_counts.index, y=team_counts.values, palette="viridis")
        plt.title('Number of Matches Played by Each Team')
        plt.xlabel('Teams')
        plt.ylabel('Number of Matches')
        plt.xticks(rotation=90)  # Rotate team names for readability
        plt.tight_layout()
        
        # Display the plot
        #plt.show()

        # Save the plot to a buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)

        # Encode the image in base64 and log it
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        #logger.info("Scatter plot image (base64 encoded):")
        #logger.info(f"data:image/png;base64,{img_base64}")

        # Save the plot as a file
        plt.savefig(".\output\plot_matches_per_team.png")
        logger.info("Scatter plot saved as 'plot_matches_per_team.png'")

def main():
    # Load and preprocess data
    data_loader = DataLoader(file_path=".\data\matches.csv")
    df = data_loader.load_data()

    # Perform basic stats and analysis
    data_analyzer = DataAnalyzer(df)
    
    summary_stats = data_analyzer.summary_statistics()
    missing_vals = data_analyzer.missing_values()
    data_types = data_analyzer.data_types()

    # since IPL team names are chnages over the year use the laters team name 
    df = data_analyzer.clean_data()
    data_analyzer.plot_matches_per_team()


if __name__ == "__main__":
    main()
