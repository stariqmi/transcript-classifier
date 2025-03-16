FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*


RUN apt-get update && \
    apt-get install -y wget curl netcat-traditional && \
    rm -rf /var/lib/apt/lists/*

# Download and make wait-for executable
RUN curl -o /usr/local/bin/wait-for https://raw.githubusercontent.com/eficode/wait-for/master/wait-for && \
    chmod +x /usr/local/bin/wait-for

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . . 

# Ensure migrations directory exists
RUN mkdir -p migrations/versions

# Set environment variables
ENV PYTHONPATH=/app

# Run migrations and start application
CMD wait-for db:5432 -- alembic upgrade head && python app.py