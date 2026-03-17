#!/usr/bin/env python3
"""
Database Connection Test Script
Tests database connectivity and configuration for Mini Uber Data Platform
"""

import os
import sys
from dotenv import load_dotenv
import mysql.connector
import yaml
from pathlib import Path

def load_config():
    """Load configuration from config.yaml"""
    config_path = Path(__file__).parent.parent / 'config' / 'config.yaml'
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print("Config file not found. Please ensure config/config.yaml exists.")
        return None
    except Exception as e:
        print(f"Error loading config: {e}")
        return None

def test_database_connection():
    """Test database connection using environment variables"""
    print("Testing database connection...")

    # Load environment variables
    load_dotenv()

    # Get database configuration
    db_config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': int(os.getenv('DB_PORT', 3306)),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),
        'database': os.getenv('DB_NAME', 'uber_data_platform')
    }

    print("Connection Details:")
    print(f"   Host: {db_config['host']}:{db_config['port']}")
    print(f"   User: {db_config['user']}")
    print(f"   Database: {db_config['database']}")
    print(f"   Password: {'*' * len(db_config['password']) if db_config['password'] else 'Not set'}")

    try:
        # Attempt connection
        print("\nAttempting to connect...")
        connection = mysql.connector.connect(**db_config)
        print("Database connection successful!")

        # Test basic query
        print("Testing basic query...")
        cursor = connection.cursor()
        cursor.execute("SELECT 1 as test_value")
        result = cursor.fetchone()
        print(f"Query executed successfully: {result}")

        # Test if our tables exist
        print("Checking if tables exist...")
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        table_names = [table[0] for table in tables]

        expected_tables = ['trips', 'drivers', 'passengers']
        existing_tables = [table for table in expected_tables if table in table_names]

        if existing_tables:
            print(f"Found tables: {', '.join(existing_tables)}")
            if len(existing_tables) < len(expected_tables):
                missing = [t for t in expected_tables if t not in existing_tables]
                print(f"Missing tables: {', '.join(missing)}")
                print("   Run: mysql -u root -p uber_data_platform < sql/schema.sql")
        else:
            print("No expected tables found. Run schema setup first.")
            print("   Run: mysql -u root -p uber_data_platform < sql/schema.sql")

        # Test data insertion (optional)
        if 'trips' in table_names:
            print("Testing data insertion...")
            try:
                cursor.execute("""
                    INSERT INTO trips (trip_id, driver_id, passenger_id, pickup_location,
                                     dropoff_location, distance_km, duration_minutes, fare_amount, timestamp)
                    VALUES (99999, 999, 999, 'Test', 'Test', 1.0, 5, 10.00, NOW())
                    ON DUPLICATE KEY UPDATE trip_id = trip_id
                """)
                connection.commit()
                print("Test data insertion successful!")

                # Clean up test data
                cursor.execute("DELETE FROM trips WHERE trip_id = 99999")
                connection.commit()
                print("Test data cleaned up!")

            except Exception as e:
                print(f"Data insertion test failed: {e}")

        cursor.close()
        connection.close()
        print("Connection closed successfully!")

        return True

    except mysql.connector.Error as e:
        print(f"Database connection failed: {e}")

        # Provide helpful error messages
        if "Access denied" in str(e):
            print("\nPossible solutions:")
            print("   1. Check your MySQL username and password in .env file")
            print("   2. Make sure MySQL server is running")
            print("   3. Verify user has access to the database")

        elif "Unknown database" in str(e):
            print("\nPossible solutions:")
            print("   1. Create the database: CREATE DATABASE uber_data_platform;")
            print("   2. Or update DB_NAME in .env file")

        elif "Can't connect" in str(e):
            print("\nPossible solutions:")
            print("   1. Start MySQL server")
            print("   2. Check if MySQL is installed and running")
            print("   3. Verify host and port in .env file")

        return False

    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def test_file_paths():
    """Test if required files exist"""
    print("\nTesting file paths...")

    # Get the project root directory (where this script is located)
    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    print(f"Project root: {project_root}")

    required_files = [
        'data/trips.csv',
        'config/config.yaml',
        '.env',
        'sql/schema.sql',
        'sql/analytics.sql'
    ]

    all_exist = True
    for file_path in required_files:
        full_path = project_root / file_path
        if full_path.exists():
            print(f"[OK] {file_path}")
        else:
            print(f"[MISSING] {file_path}")
            all_exist = False

    # Also check for optional files
    optional_files = [
        'logs/etl_pipeline.log',
        'data/trips_cleaned.csv',
        'README.md',
        'requirements.txt'
    ]

    print("\nOptional files:")
    for file_path in optional_files:
        full_path = project_root / file_path
        if full_path.exists():
            print(f"[OK] {file_path}")
        else:
            print(f"[NOT CREATED] {file_path} - Not created yet")

    return all_exist

def main():
    """Main test function"""
    print("Mini Uber Data Platform - Connection Test")
    print("=" * 50)

    # Test file paths
    files_ok = test_file_paths()

    # Test database connection
    db_ok = test_database_connection()

    print("\n" + "=" * 50)
    print("Test Results:")

    if files_ok and db_ok:
        print("ALL TESTS PASSED! Your setup is ready.")
        print("You can now run: python pipelines/etl_pipeline.py")
        return 0
    else:
        print("Some tests failed. Please fix the issues above.")
        if not files_ok:
            print("   - Check that all required files exist")
        if not db_ok:
            print("   - Fix database connection issues")
        return 1

if __name__ == "__main__":
    sys.exit(main())
