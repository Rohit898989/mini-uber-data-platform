# Database Schema Documentation

## Entity Relationship Diagram

```
+----------------+     +------------------+     +--------------------+
|     trips      |     |    drivers       |     |   passengers       |
+----------------+     +------------------+     +--------------------+
| trip_id (PK)   |     | driver_id (PK)   |     | passenger_id (PK)  |
| driver_id (FK) | --> | name             |     | name               |
| passenger_id(FK|     | email            |     | email              |
| pickup_loc     |     | phone            |     | phone              |
| dropoff_loc    |     | rating           |     | total_trips        |
| distance_km    |     | total_trips      |     | joined_date        |
| duration_min   |     | joined_date      |     +--------------------+
| fare_amount    |     +------------------+
| timestamp      |
| created_at     |
+----------------+
```

## Table Relationships

- **trips.driver_id** → **drivers.driver_id** (Many-to-One)
- **trips.passenger_id** → **passengers.passenger_id** (Many-to-One)

## Data Flow

1. **Raw Data** → ETL Pipeline → **Clean Data**
2. **Clean Data** → Database → **Analytics**
3. **Analytics** → Reports → **Business Insights**

## Schema Version History

- **v1.0** - Initial schema with basic trip tracking
- **v1.1** - Added driver and passenger tables
- **v1.2** - Added indexes for performance
- **v1.3** - Added audit timestamps