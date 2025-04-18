FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt faker click

# Copy application code
COPY . .

# Make instance directory writable
RUN mkdir -p /app/instance && chmod 777 /app/instance

# Make scripts executable
RUN chmod +x entrypoint.sh
RUN chmod +x scripts/*.py

EXPOSE 5000

# Set environment variables
ENV FLASK_APP=run.py
ENV FLASK_CONFIG=development
ENV FLASK_DEBUG=1
ENV PYTHONPATH=/app
# Explicitly set the database URL for SQLite
ENV DATABASE_URL="sqlite:////app/instance/sqlitedb.file"

# Run entrypoint script
ENTRYPOINT ["./entrypoint.sh"]