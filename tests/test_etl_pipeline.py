import pytest
import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from pipelines.etl_pipeline import extract_data, transform_data, load_data

class TestETLPipeline:
    """Test cases for the ETL pipeline functions"""

    def test_extract_data_success(self):
        """Test successful data extraction from CSV"""
        # Setup test data
        test_data_path = project_root / "data" / "trips.csv"

        # Execute
        result = extract_data(str(test_data_path))

        # Assert
        assert isinstance(result, list)
        assert len(result) > 0
        assert "trip_id" in result[0]
        assert "driver_id" in result[0]

    def test_transform_data_validation(self):
        """Test data transformation and validation"""
        # Setup test data
        test_data = [
            {"trip_id": "1", "distance_km": "5.2", "duration_minutes": "15", "fare_amount": "18.50"},
            {"trip_id": "2", "distance_km": "8.1", "duration_minutes": "invalid", "fare_amount": "25.75"},
        ]

        # Execute
        result = transform_data(test_data)

        # Assert - should filter out invalid records
        assert len(result) == 1
        assert result[0]["trip_id"] == "1"
        assert isinstance(result[0]["distance_km"], float)

    def test_load_data_creates_file(self, tmp_path):
        """Test data loading creates output file"""
        # Setup test data
        test_data = [
            {"trip_id": "1", "driver_id": "101", "passenger_id": "201", "pickup_location": "Manhattan"}
        ]

        # Execute
        output_file = tmp_path / "test_output.csv"
        load_data(test_data, str(output_file))

        # Assert
        assert output_file.exists()
        assert output_file.stat().st_size > 0

    def test_data_types_conversion(self):
        """Test that string data is properly converted to correct types"""
        # Setup test data
        test_data = [
            {"trip_id": "1", "distance_km": "5.2", "duration_minutes": "15", "fare_amount": "18.50"}
        ]

        # Execute
        result = transform_data(test_data)

        # Assert data types
        assert isinstance(result[0]["distance_km"], float)
        assert isinstance(result[0]["duration_minutes"], int)
        assert isinstance(result[0]["fare_amount"], float)

if __name__ == "__main__":
    pytest.main([__file__])