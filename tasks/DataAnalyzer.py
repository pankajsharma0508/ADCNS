import logging
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
# Configure standard logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

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
        plt.show()