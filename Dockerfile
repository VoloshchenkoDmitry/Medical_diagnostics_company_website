FROM python:3.13-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY src/ .

# Create static and media directories
RUN mkdir -p static media

# Run the application
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
