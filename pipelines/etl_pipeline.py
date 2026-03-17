import csv
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    filename='logs/etl_pipeline.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

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
    input_file = "data/trips.csv"
    output_file = "data/trips_cleaned.csv"
    
    trips = extract_data(input_file)
    cleaned_trips = transform_data(trips)
    load_data(cleaned_trips, output_file)
    
    logging.info("ETL pipeline completed successfully")
    print("✅ ETL pipeline completed successfully")
