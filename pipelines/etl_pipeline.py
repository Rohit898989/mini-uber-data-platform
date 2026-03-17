import csv
import logging
import os
from datetime import datetime
from dotenv import load_dotenv
import yaml

# Load environment variables from .env file
load_dotenv()

# Load configuration from YAML file
def load_config():
    """Load configuration from config.yaml"""
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

# Get configuration
config = load_config()

# Configure logging from config
logging.basicConfig(
    filename=config['logging']['file_path'],
    level=getattr(logging, config['logging']['level']),
    format=config['logging']['format']
)

# Database configuration from environment variables
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'uber_data_platform')
}

# Pipeline configuration
BATCH_SIZE = int(os.getenv('BATCH_SIZE', config['pipeline']['batch_size']))
LOG_LEVEL = os.getenv('LOG_LEVEL', config['logging']['level'])
ENABLE_CACHE = os.getenv('ENABLE_CACHE', 'true').lower() == 'true'

# Data paths from environment or config
DATA_INPUT_PATH = os.getenv('DATA_INPUT_PATH', config['data']['input']['path'])
DATA_OUTPUT_PATH = os.getenv('DATA_OUTPUT_PATH', config['data']['output']['path'])
LOG_PATH = os.getenv('LOG_PATH', config['logging']['file_path'])

def extract_data(input_file):
    """Extract data from CSV file"""
    logging.info(f"Extracting data from {input_file}")
    trips = []
    with open(input_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            trips.append(row)
    logging.info(f"Extracted {len(trips)} records")
    return trips

def transform_data(trips):
    """Transform and clean data"""
    logging.info("Transforming data...")
    cleaned_trips = []
    for trip in trips:
        try:
            trip['distance_km'] = float(trip['distance_km'])
            trip['duration_minutes'] = int(trip['duration_minutes'])
            trip['fare_amount'] = float(trip['fare_amount'])
            cleaned_trips.append(trip)
        except (ValueError, KeyError) as e:
            logging.warning(f"Skipping invalid record: {trip}")
    logging.info(f"Transformed {len(cleaned_trips)} records")
    return cleaned_trips

def load_data(trips, output_file):
    """Load data to output file"""
    logging.info(f"Loading data to {output_file}")
    # In production, this would load to a database
    with open(output_file, 'w', newline='') as file:
        if trips:
            fieldnames = trips[0].keys()
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(trips)
    logging.info(f"Loaded {len(trips)} records")

if __name__ == "__main__":
    logging.info("Starting ETL pipeline execution")
    logging.info(f"Batch size: {BATCH_SIZE}")
    logging.info(f"Input file: {DATA_INPUT_PATH}")
    logging.info(f"Output file: {DATA_OUTPUT_PATH}")

    try:
        # Extract
        trips = extract_data(DATA_INPUT_PATH)
        logging.info(f"Successfully extracted {len(trips)} records")

        # Transform
        cleaned_trips = transform_data(trips)
        logging.info(f"Successfully transformed {len(cleaned_trips)} records")

        # Load
        load_data(cleaned_trips, DATA_OUTPUT_PATH)
        logging.info("ETL pipeline completed successfully")

        print("ETL pipeline completed successfully")
        print(f"Processed {len(cleaned_trips)} records")
        print(f"Output saved to: {DATA_OUTPUT_PATH}")

    except Exception as e:
        logging.error(f"ETL pipeline failed: {str(e)}")
        print(f"ETL pipeline failed: {str(e)}")
        raise
