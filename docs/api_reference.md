# API Reference

## Overview

The Mini Uber Data Platform provides REST API endpoints for data access and analytics. This document describes the available endpoints and their usage.

## Base URL
```
http://localhost:5000/api/v1
```

## Authentication
Currently, no authentication is required. In production, implement JWT or API key authentication.

## Endpoints

### GET /health
Check API health status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "1.0.0"
}
```

### GET /trips
Retrieve trip data with optional filtering.

**Query Parameters:**
- `limit` (int): Maximum number of records (default: 100)
- `offset` (int): Pagination offset (default: 0)
- `start_date` (string): Filter by start date (YYYY-MM-DD)
- `end_date` (string): Filter by end date (YYYY-MM-DD)

**Example:**
```
GET /api/v1/trips?limit=50&start_date=2024-01-01
```

**Response:**
```json
{
  "data": [
    {
      "trip_id": 1,
      "driver_id": 101,
      "passenger_id": 201,
      "pickup_location": "Manhattan",
      "dropoff_location": "Brooklyn",
      "distance_km": 5.2,
      "duration_minutes": 15,
      "fare_amount": 18.50,
      "timestamp": "2024-01-01T08:00:00Z"
    }
  ],
  "total": 1,
  "limit": 50,
  "offset": 0
}
```

### GET /analytics/revenue
Get revenue analytics data.

**Query Parameters:**
- `period` (string): "daily", "weekly", "monthly" (default: "daily")
- `days` (int): Number of days to look back (default: 30)

**Response:**
```json
{
  "period": "daily",
  "data": [
    {
      "date": "2024-01-15",
      "trips": 45,
      "revenue": 1250.75,
      "avg_fare": 27.79
    }
  ]
}
```

### GET /drivers/top
Get top-performing drivers.

**Query Parameters:**
- `limit` (int): Number of drivers to return (default: 10)
- `metric` (string): "earnings", "trips", "rating" (default: "earnings")

**Response:**
```json
{
  "metric": "earnings",
  "drivers": [
    {
      "driver_id": 101,
      "name": "John Smith",
      "trips": 150,
      "earnings": 4250.00,
      "rating": 4.8
    }
  ]
}
```

## Error Responses

All errors follow this format:
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid date format",
    "details": {
      "field": "start_date",
      "expected": "YYYY-MM-DD"
    }
  }
}
```

## Rate Limiting
- 1000 requests per hour per IP
- 10000 requests per day per IP

## Future Endpoints (Planned)

### POST /trips
Create new trip records.

### PUT /drivers/{id}
Update driver information.

### DELETE /trips/{id}
Delete trip records (admin only).

## Data Formats

All dates use ISO 8601 format: `YYYY-MM-DDTHH:MM:SSZ`
All monetary values are in USD with 2 decimal places.
All distances are in kilometers.
All durations are in minutes.