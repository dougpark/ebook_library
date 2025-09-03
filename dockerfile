# Use official Python 3.12 image
FROM python:3.12-slim

# Set work directory
WORKDIR /app

# Copy Python files
# COPY . /app

# Copy dependencies only (optional, speeds up rebuilds)
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 5100

# Run the app
CMD ["python", "app.py"]
