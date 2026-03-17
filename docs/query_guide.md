# SQL Query Guide

## Analytics Queries Overview

This document provides detailed explanations of all analytics queries used in the Mini Uber Data Platform.

## 1. Revenue Dashboard Query

```sql
SELECT
    DATE(timestamp) AS trip_date,
    COUNT(*) AS total_trips,
    ROUND(SUM(fare_amount), 2) AS total_revenue,
    ROUND(AVG(fare_amount), 2) AS avg_fare
FROM trips
GROUP BY DATE(timestamp)
ORDER BY trip_date DESC;
```

**Purpose:** Daily revenue and trip metrics
**Use Case:** Monitor business performance over time
**Output:** Date, trip count, revenue, average fare

## 2. Top Drivers Query

```sql
SELECT
    d.name,
    COUNT(t.trip_id) AS trips,
    ROUND(SUM(t.fare_amount), 2) AS earnings,
    ROUND(AVG(d.rating), 1) AS rating
FROM drivers d
LEFT JOIN trips t ON d.driver_id = t.driver_id
GROUP BY d.driver_id
ORDER BY earnings DESC
LIMIT 10;
```

**Purpose:** Identify highest-performing drivers
**Use Case:** Driver performance analysis and incentives
**Output:** Driver name, trip count, earnings, rating

## 3. Location Heatmap Query

```sql
SELECT
    pickup_location,
    COUNT(*) AS demand,
    ROUND(AVG(fare_amount), 2) AS avg_fare
FROM trips
GROUP BY pickup_location
ORDER BY demand DESC;
```

**Purpose:** Analyze pickup location demand
**Use Case:** Optimize driver placement and pricing
**Output:** Location, demand count, average fare

## Performance Optimization Tips

### Indexes Used
- `idx_driver_id` on trips.driver_id
- `idx_passenger_id` on trips.passenger_id
- `idx_timestamp` on trips.timestamp

### Query Performance
- All queries use indexed columns for filtering
- GROUP BY operations are optimized
- LIMIT clauses prevent large result sets

## Custom Query Examples

### Monthly Revenue Trend
```sql
SELECT
    DATE_FORMAT(timestamp, '%Y-%m') AS month,
    COUNT(*) AS trips,
    SUM(fare_amount) AS revenue
FROM trips
GROUP BY month
ORDER BY month;
```

### Peak Hours Analysis
```sql
SELECT
    HOUR(timestamp) AS hour,
    COUNT(*) AS trips,
    AVG(fare_amount) AS avg_fare
FROM trips
GROUP BY hour
ORDER BY trips DESC;
```