# Base image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code to the container
COPY website/ /app/website/
COPY main.py /app/

# Expose port
EXPOSE 5000

# Run the application
CMD ["flask", "run", "--host=0.0.0.0"]
# By default, Flask runs on 127.0.0.1 (localhost) which only allows connections from within the container,
# but by setting the host to 0.0.0.0 tells Flask to listen on all available network interfaces