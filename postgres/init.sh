#!/bin/bash
set -e

# Create database and user using the defined environment variables
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE TABLE IF NOT EXISTS sample_data (
        id SERIAL PRIMARY KEY,
        content TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    INSERT INTO sample_data (content) VALUES 
    ('Successful initialization - Data Point 1'),
    ('System operational - Data Point 2');
EOSQL

