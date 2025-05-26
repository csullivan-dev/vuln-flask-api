#!/bin/bash

echo "Checking instance directory..."
if [ -d "/app/instance" ] && [ -w "/app/instance" ]; then
    echo "Instance directory exists and is writable"
else
    echo "Making instance directory writable..."
    mkdir -p /app/instance
    chmod 777 /app/instance
fi

# Set this explicitly for SQLite
export FLASK_APP=run.py
export FLASK_CONFIG=development
export FLASK_DEBUG=1  # Use this instead of FLASK_ENV

# Ensure the database URI is properly set
export DATABASE_URL="sqlite:////app/instance/sqlitedb.file"

echo "Initializing database..."
cd /app

# Create a database file with proper permissions
touch /app/instance/sqlitedb.file
chmod 666 /app/instance/sqlitedb.file
ls -la /app/instance

# Run the init_db.py script
python scripts/init_db.py

# Run generate_sample_data.py with the appropriate click parameters
python scripts/generate_sample_data.py --users 200 --posts 200

echo "Starting Flask application..."
python run.py