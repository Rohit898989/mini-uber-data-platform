import pytest
import os
import csv
from pathlib import Path

class TestDataQuality:
    """Test cases for data quality validation"""

    def test_csv_file_exists(self):
        """Test that required CSV files exist"""
        project_root = Path(__file__).parent.parent
        data_dir = project_root / "data"

        assert (data_dir / "trips.csv").exists()
        assert (data_dir / "trips_cleaned.csv").exists()

    def test_csv_headers_valid(self):
        """Test that CSV files have valid headers"""
        project_root = Path(__file__).parent.parent
        trips_file = project_root / "data" / "trips.csv"

        with open(trips_file, 'r') as f:
            reader = csv.reader(f)
            headers = next(reader)

        expected_headers = ["trip_id", "driver_id", "passenger_id",
                          "pickup_location", "dropoff_location",
                          "distance_km", "duration_minutes", "fare_amount", "timestamp"]

        assert len(headers) == len(expected_headers)
        for header in expected_headers:
            assert header in headers

    def test_data_integrity(self):
        """Test data integrity constraints"""
        project_root = Path(__file__).parent.parent
        trips_file = project_root / "data" / "trips.csv"

        with open(trips_file, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        # Test that all rows have required fields
        for row in rows:
            assert row["trip_id"]
            assert row["driver_id"]
            assert row["passenger_id"]
            assert row["pickup_location"]
            assert row["dropoff_location"]

    def test_numeric_data_valid(self):
        """Test that numeric fields contain valid numbers"""
        project_root = Path(__file__).parent.parent
        trips_file = project_root / "data" / "trips.csv"

        with open(trips_file, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        for row in rows:
            # Test numeric conversions
            try:
                float(row["distance_km"])
                int(row["duration_minutes"])
                float(row["fare_amount"])
            except (ValueError, TypeError):
                pytest.fail(f"Invalid numeric data in row: {row}")

    def test_no_duplicate_trip_ids(self):
        """Test that trip IDs are unique"""
        project_root = Path(__file__).parent.parent
        trips_file = project_root / "data" / "trips.csv"

        with open(trips_file, 'r') as f:
            reader = csv.DictReader(f)
            trip_ids = [row["trip_id"] for row in reader]

        assert len(trip_ids) == len(set(trip_ids)), "Duplicate trip IDs found"

    def test_location_data_reasonable(self):
        """Test that location data is reasonable"""
        project_root = Path(__file__).parent.parent
        trips_file = project_root / "data" / "trips.csv"

        with open(trips_file, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        valid_locations = ["Manhattan", "Brooklyn", "Queens", "Bronx", "Staten Island"]

        for row in rows:
            assert row["pickup_location"] in valid_locations
            assert row["dropoff_location"] in valid_locations

if __name__ == "__main__":
    pytest.main([__file__])