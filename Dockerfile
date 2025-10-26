FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project files (copy contents of src to /app)
COPY src/ .

# Create necessary directories
RUN mkdir -p static media

# Expose port
EXPOSE 8000

# Command to run migrations and start server
CMD ["sh", "-c", "sleep 10 && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]