import logging

# Configure standard logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

class CleanData:
    def __init__(self, df):
        self.df = df

    def clean_data(self):
        logger.info("Cleaning up teams names from the dataset:")
        team = self.df.describe(include='all')
        team_counts = self.df['team1'].value_counts()
        logger.info('IPL teams list ')
        logger.info(team_counts)
        # Replace 'Delhi Daredevils' with 'Delhi Capitals' in the 'team' column
        team = team['team1'].replace('Delhi Daredevils', 'Delhi Capitals')
        team = team['team1'].replace('Deccan Chargers ', 'Sunrisers Hyderabad')
        #team = team.replace('Deccan Chargers ', 'Sunrisers Hyderabad')

        logger.info(f"\n replaced team names  ")
        team_counts = self.df.value_counts()
        logger.info(team_counts)

        