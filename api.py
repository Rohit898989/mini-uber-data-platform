#!/usr/bin/env python3
"""
Mini Uber Data Platform API Server
REST API for accessing trip data and analytics
"""

import os
import sys
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from dotenv import load_dotenv
import yaml
from pathlib import Path

# Load environment variables
load_dotenv()

# Load configuration
def load_config():
    """Load configuration from config.yaml"""
    config_path = Path(__file__).parent / 'config' / 'config.yaml'
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        return None

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database configuration
def get_db_connection():
    """Create database connection"""
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=int(os.getenv('DB_PORT', 3306)),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'uber_data_platform'),
            connection_timeout=5  # Add timeout
        )
        return connection
    except mysql.connector.Error as e:
        print(f"Database connection error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected database error: {e}")
        return None

@app.route('/api/v1/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        # Test database connection
        conn = get_db_connection()
        if conn:
            conn.close()
            db_status = "connected"
        else:
            db_status = "disconnected"

        return jsonify({
            "status": "healthy" if db_status == "connected" else "degraded",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "version": "1.0.0",
            "database": db_status,
            "message": "API is running but database is not connected" if db_status == "disconnected" else "All systems operational"
        }), 200 if db_status == "connected" else 200  # Return 200 even if DB is down for health check

    except Exception as e:
        return jsonify({
            "status": "error",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "version": "1.0.0",
            "error": str(e)
        }), 500

@app.route('/api/v1/trips', methods=['GET'])
def get_trips():
    """Get trip data with optional filtering"""
    try:
        # Get query parameters
        limit = int(request.args.get('limit', 100))
        offset = int(request.args.get('offset', 0))
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        # Validate limit
        if limit > 1000:
            limit = 1000
        if limit < 1:
            limit = 1

        # Build query
        query = """
        SELECT
            t.trip_id,
            t.driver_id,
            t.passenger_id,
            t.pickup_location,
            t.dropoff_location,
            t.distance_km,
            t.duration_minutes,
            t.fare_amount,
            t.timestamp,
            d.name as driver_name,
            p.name as passenger_name
        FROM trips t
        LEFT JOIN drivers d ON t.driver_id = d.driver_id
        LEFT JOIN passengers p ON t.passenger_id = p.passenger_id
        WHERE 1=1
        """

        params = []

        # Add date filters
        if start_date:
            query += " AND DATE(t.timestamp) >= %s"
            params.append(start_date)

        if end_date:
            query += " AND DATE(t.timestamp) <= %s"
            params.append(end_date)

        # Add ordering and pagination
        query += " ORDER BY t.timestamp DESC LIMIT %s OFFSET %s"
        params.extend([limit, offset])

        # Execute query
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params)
        trips = cursor.fetchall()

        # Get total count for pagination
        count_query = """
        SELECT COUNT(*) as total
        FROM trips t
        WHERE 1=1
        """
        count_params = []

        if start_date:
            count_query += " AND DATE(t.timestamp) >= %s"
            count_params.append(start_date)

        if end_date:
            count_query += " AND DATE(t.timestamp) <= %s"
            count_params.append(end_date)

        cursor.execute(count_query, count_params)
        total = cursor.fetchone()['total']

        cursor.close()
        conn.close()

        # Format response
        response_data = []
        for trip in trips:
            response_data.append({
                "trip_id": trip['trip_id'],
                "driver_id": trip['driver_id'],
                "passenger_id": trip['passenger_id'],
                "pickup_location": trip['pickup_location'],
                "dropoff_location": trip['dropoff_location'],
                "distance_km": float(trip['distance_km']),
                "duration_minutes": int(trip['duration_minutes']),
                "fare_amount": float(trip['fare_amount']),
                "timestamp": trip['timestamp'].isoformat() + "Z" if trip['timestamp'] else None,
                "driver_name": trip['driver_name'],
                "passenger_name": trip['passenger_name']
            })

        return jsonify({
            "data": response_data,
            "total": total,
            "limit": limit,
            "offset": offset
        })

    except Exception as e:
        return jsonify({"error": f"Failed to fetch trips: {str(e)}"}), 500

@app.route('/api/v1/analytics/revenue', methods=['GET'])
def get_revenue_analytics():
    """Get revenue analytics data"""
    try:
        period = request.args.get('period', 'daily')
        days = int(request.args.get('days', 30))

        # Validate period
        if period not in ['daily', 'weekly', 'monthly']:
            period = 'daily'

        # Validate days
        if days > 365:
            days = 365
        if days < 1:
            days = 1

        # Build query based on period
        if period == 'daily':
            date_format = '%Y-%m-%d'
            group_by = "DATE(t.timestamp)"
        elif period == 'weekly':
            date_format = '%Y-%U'
            group_by = "YEARWEEK(t.timestamp, 1)"
        else:  # monthly
            date_format = '%Y-%m'
            group_by = "DATE_FORMAT(t.timestamp, '%Y-%m')"

        query = f"""
        SELECT
            DATE_FORMAT(t.timestamp, '{date_format}') as period,
            COUNT(*) as trips,
            SUM(t.fare_amount) as revenue,
            AVG(t.fare_amount) as avg_fare,
            SUM(t.distance_km) as total_distance
        FROM trips t
        WHERE t.timestamp >= DATE_SUB(CURDATE(), INTERVAL {days} DAY)
        GROUP BY {group_by}
        ORDER BY period DESC
        """

        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()

        cursor.close()
        conn.close()

        # Format response
        response_data = []
        for row in results:
            response_data.append({
                "period": row['period'],
                "trips": int(row['trips']),
                "revenue": float(row['revenue']) if row['revenue'] else 0.0,
                "avg_fare": float(row['avg_fare']) if row['avg_fare'] else 0.0,
                "total_distance": float(row['total_distance']) if row['total_distance'] else 0.0
            })

        return jsonify({
            "period": period,
            "days": days,
            "data": response_data
        })

    except Exception as e:
        return jsonify({"error": f"Failed to fetch revenue analytics: {str(e)}"}), 500

@app.route('/api/v1/drivers/top', methods=['GET'])
def get_top_drivers():
    """Get top-performing drivers"""
    try:
        limit = int(request.args.get('limit', 10))
        metric = request.args.get('metric', 'earnings')

        # Validate limit
        if limit > 50:
            limit = 50
        if limit < 1:
            limit = 1

        # Validate metric
        valid_metrics = ['earnings', 'trips', 'rating']
        if metric not in valid_metrics:
            metric = 'earnings'

        # Build query based on metric
        if metric == 'earnings':
            order_by = "SUM(t.fare_amount) DESC"
            metric_field = "SUM(t.fare_amount)"
        elif metric == 'trips':
            order_by = "COUNT(t.trip_id) DESC"
            metric_field = "COUNT(t.trip_id)"
        else:  # rating - for now, we'll use a calculated rating
            order_by = "AVG(t.fare_amount / t.distance_km) DESC"  # efficiency rating
            metric_field = "AVG(t.fare_amount / t.distance_km)"

        query = f"""
        SELECT
            d.driver_id,
            d.name,
            COUNT(t.trip_id) as trips,
            COALESCE(SUM(t.fare_amount), 0) as earnings,
            COALESCE(AVG(t.fare_amount), 0) as avg_fare,
            COALESCE(AVG(t.distance_km), 0) as avg_distance,
            COALESCE(AVG(t.fare_amount / NULLIF(t.distance_km, 0)), 0) as efficiency_rating
        FROM drivers d
        LEFT JOIN trips t ON d.driver_id = t.driver_id
        GROUP BY d.driver_id, d.name
        HAVING trips > 0
        ORDER BY {order_by}
        LIMIT %s
        """

        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, [limit])
        results = cursor.fetchall()

        cursor.close()
        conn.close()

        # Format response
        response_data = []
        for row in results:
            response_data.append({
                "driver_id": row['driver_id'],
                "name": row['name'],
                "trips": int(row['trips']),
                "earnings": float(row['earnings']),
                "avg_fare": float(row['avg_fare']),
                "avg_distance": float(row['avg_distance']),
                "efficiency_rating": float(row['efficiency_rating'])
            })

        return jsonify({
            "metric": metric,
            "limit": limit,
            "drivers": response_data
        })

    except Exception as e:
        return jsonify({"error": f"Failed to fetch top drivers: {str(e)}"}), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    # Get configuration
    config = load_config()
    debug = config.get('api', {}).get('debug', False) if config else False
    host = config.get('api', {}).get('host', '0.0.0.0') if config else '0.0.0.0'
    port = config.get('api', {}).get('port', 5000) if config else 5000

    # Override with environment variables if set
    host = os.getenv('API_HOST', host)
    port = int(os.getenv('API_PORT', port))
    debug = os.getenv('API_DEBUG', str(debug)).lower() == 'true'

    print(f"Starting Mini Uber Data Platform API Server...")
    print(f"Host: {host}")
    print(f"Port: {port}")
    print(f"Debug: {debug}")
    print(f"API Base URL: http://localhost:{port}/api/v1")
    print("=" * 50)

    app.run(host=host, port=port, debug=debug)