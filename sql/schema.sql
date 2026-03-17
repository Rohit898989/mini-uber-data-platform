-- Create trips table
CREATE TABLE IF NOT EXISTS trips (
    trip_id INT PRIMARY KEY,
    driver_id INT NOT NULL,
    passenger_id INT NOT NULL,
    pickup_location VARCHAR(100),
    dropoff_location VARCHAR(100),
    distance_km DECIMAL(10, 2),
    duration_minutes INT,
    fare_amount DECIMAL(10, 2),
    timestamp DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Create drivers table
CREATE TABLE IF NOT EXISTS drivers (
    driver_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(15),
    rating DECIMAL(3, 2),
    total_trips INT DEFAULT 0,
    joined_date DATE
);

-- Create passengers table
CREATE TABLE IF NOT EXISTS passengers (
    passenger_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(15),
    total_trips INT DEFAULT 0,
    joined_date DATE
);

-- Create indexes for better query performance
CREATE INDEX idx_driver_id ON trips(driver_id);
CREATE INDEX idx_passenger_id ON trips(passenger_id);
CREATE INDEX idx_timestamp ON trips(timestamp);
