-- Analytics queries for mini-uber data platform

-- 1. Total trips and revenue by date
SELECT 
    DATE(timestamp) AS trip_date,
    COUNT(*) AS total_trips,
    SUM(fare_amount) AS total_revenue,
    AVG(fare_amount) AS avg_fare,
    AVG(distance_km) AS avg_distance
FROM trips
GROUP BY DATE(timestamp)
ORDER BY trip_date DESC;

-- 2. Top 10 drivers by trip count
SELECT 
    d.driver_id,
    d.name,
    COUNT(t.trip_id) AS total_trips,
    SUM(t.fare_amount) AS total_earnings,
    AVG(t.duration_minutes) AS avg_trip_duration,
    AVG(d.rating) AS avg_rating
FROM drivers d
LEFT JOIN trips t ON d.driver_id = t.driver_id
GROUP BY d.driver_id, d.name
ORDER BY total_trips DESC
LIMIT 10;

-- 3. Top 10 passengers by trip frequency
SELECT 
    p.passenger_id,
    p.name,
    COUNT(t.trip_id) AS total_trips,
    SUM(t.fare_amount) AS total_spent,
    AVG(t.distance_km) AS avg_distance
FROM passengers p
LEFT JOIN trips t ON p.passenger_id = t.passenger_id
GROUP BY p.passenger_id, p.name
ORDER BY total_trips DESC
LIMIT 10;

-- 4. Average metrics by location
SELECT 
    pickup_location,
    COUNT(*) AS trip_count,
    AVG(distance_km) AS avg_distance,
    AVG(duration_minutes) AS avg_duration,
    AVG(fare_amount) AS avg_fare
FROM trips
GROUP BY pickup_location
ORDER BY trip_count DESC;

-- 5. Revenue metrics
SELECT 
    COUNT(*) AS total_trips,
    SUM(fare_amount) AS total_revenue,
    AVG(fare_amount) AS avg_fare_per_trip,
    MIN(fare_amount) AS min_fare,
    MAX(fare_amount) AS max_fare,
    STDDEV(fare_amount) AS fare_stddev
FROM trips;
