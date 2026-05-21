FROM python:3.11-slim

WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Expose application port
EXPOSE 5000

# Environment variables
ENV ENVIRONMENT=development
ENV PLATFORM_TEAM=platform-engineering
ENV VERSION=v1

CMD ["python", "app.py"]