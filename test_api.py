#!/usr/bin/env python3
"""
API Test Script for Mini Uber Data Platform
Tests all API endpoints to verify they work correctly
"""

import requests
import json
import time
from pathlib import Path

# API base URL
BASE_URL = "http://localhost:5000/api/v1"

def test_health_endpoint():
    """Test the health check endpoint"""
    print("Testing /api/v1/health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print("Response:", json.dumps(data, indent=2))
            print("✅ Health endpoint working!")
            return True
        else:
            print(f"❌ Health endpoint failed with status {response.status_code}")
            return False

    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API server. Is it running?")
        print("   Start the server with: python api.py")
        return False
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")
        return False

def test_trips_endpoint():
    """Test the trips endpoint"""
    print("\nTesting /api/v1/trips endpoint...")
    try:
        # Test basic request
        response = requests.get(f"{BASE_URL}/trips", timeout=10)
        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"Total trips: {data.get('total', 'N/A')}")
            print(f"Returned trips: {len(data.get('data', []))}")
            print("Sample trip data:")
            if data.get('data'):
                print(json.dumps(data['data'][0], indent=2))
            print("✅ Trips endpoint working!")
            return True
        else:
            error_data = response.json()
            print(f"❌ Trips endpoint failed: {error_data.get('error', 'Unknown error')}")
            return False

    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API server")
        return False
    except Exception as e:
        print(f"❌ Trips endpoint error: {e}")
        return False

def test_revenue_analytics():
    """Test the revenue analytics endpoint"""
    print("\nTesting /api/v1/analytics/revenue endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/analytics/revenue", timeout=10)
        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"Period: {data.get('period', 'N/A')}")
            print(f"Data points: {len(data.get('data', []))}")
            if data.get('data'):
                print("Sample revenue data:")
                print(json.dumps(data['data'][0], indent=2))
            print("✅ Revenue analytics endpoint working!")
            return True
        else:
            error_data = response.json()
            print(f"❌ Revenue analytics failed: {error_data.get('error', 'Unknown error')}")
            return False

    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API server")
        return False
    except Exception as e:
        print(f"❌ Revenue analytics error: {e}")
        return False

def test_top_drivers():
    """Test the top drivers endpoint"""
    print("\nTesting /api/v1/drivers/top endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/drivers/top", timeout=10)
        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"Metric: {data.get('metric', 'N/A')}")
            print(f"Drivers returned: {len(data.get('drivers', []))}")
            if data.get('drivers'):
                print("Top driver:")
                print(json.dumps(data['drivers'][0], indent=2))
            print("✅ Top drivers endpoint working!")
            return True
        else:
            error_data = response.json()
            print(f"❌ Top drivers failed: {error_data.get('error', 'Unknown error')}")
            return False

    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API server")
        return False
    except Exception as e:
        print(f"❌ Top drivers error: {e}")
        return False

def test_with_filters():
    """Test endpoints with query parameters"""
    print("\nTesting endpoints with filters...")

    # Test trips with limit
    try:
        response = requests.get(f"{BASE_URL}/trips?limit=5", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Trips with limit=5: returned {len(data.get('data', []))} trips")
        else:
            print("❌ Trips with limit filter failed")
    except:
        print("❌ Trips with limit filter error")

    # Test revenue analytics with different period
    try:
        response = requests.get(f"{BASE_URL}/analytics/revenue?period=weekly&days=7", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Revenue analytics with weekly period: {len(data.get('data', []))} data points")
        else:
            print("❌ Revenue analytics with period filter failed")
    except:
        print("❌ Revenue analytics with period filter error")

def main():
    """Main test function"""
    print("🚕 Mini Uber Data Platform API Test")
    print("=" * 50)
    print(f"Testing API at: {BASE_URL}")
    print("Make sure the API server is running: python api.py")
    print("=" * 50)

    # Wait a moment for server to be ready
    print("Waiting for server to be ready...")
    time.sleep(2)

    # Test all endpoints
    results = []
    results.append(test_health_endpoint())
    results.append(test_trips_endpoint())
    results.append(test_revenue_analytics())
    results.append(test_top_drivers())
    test_with_filters()

    print("\n" + "=" * 50)
    print("API Test Results:")

    successful = sum(results)
    total = len(results)

    if successful == total:
        print(f"🎉 ALL TESTS PASSED! ({successful}/{total})")
        print("\nYour API is working perfectly!")
        print("\n📋 Available endpoints:")
        print(f"   Health Check:  {BASE_URL}/health")
        print(f"   Get Trips:     {BASE_URL}/trips")
        print(f"   Revenue Data:  {BASE_URL}/analytics/revenue")
        print(f"   Top Drivers:   {BASE_URL}/drivers/top")
        print("\n🔗 Test in browser or use tools like:")
        print("   curl, Postman, or your web browser")
    else:
        print(f"⚠️  Some tests failed ({successful}/{total})")
        print("\nPossible issues:")
        print("   1. API server not running")
        print("   2. Database not connected")
        print("   3. Firewall blocking port 5000")
        print("   4. Wrong API URL")

    print("\n💡 To start the API server:")
    print("   python api.py")
    print("\n💡 To test individual endpoints:")
    print("   python test_api.py")

if __name__ == "__main__":
    main()