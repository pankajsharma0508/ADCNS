import pandas as pd
import logging

# Configure standard logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Load the dataset
df = pd.read_csv("../data/matches.csv")
logger.info("Dataset loaded successfully.")
logger.info(f"DataFrame head:\n{df.head()}")

print(df)
