# Build stage
FROM python:3.10.4-slim-bullseye as builder

WORKDIR /code

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.10.4-slim-bullseye

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1 \
    PYTHONDONTWRITEBYTECODE 1 \
    PYTHONUNBUFFERED 1

WORKDIR /code

# Copy project files
COPY . .

# Command to run the application
CMD ["python", "/code/manage.py", "runserver", "0.0.0.0:8000"]

 # Dockerfile.web-app

# /Users/mshittu/programming-projects/python/django/media-be/Dockerfile