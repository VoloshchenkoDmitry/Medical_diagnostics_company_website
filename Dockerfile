FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY src/ .

# Create necessary directories
RUN mkdir -p /app/static /app/media /app/logs

# Expose port
EXPOSE 8000

# Run application
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]