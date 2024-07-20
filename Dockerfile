# Use an official Python runtime as a parent image
FROM python:3.10.11-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the entire local directory into the container at /app
COPY . .

# Update package lists and install necessary system packages
RUN apt-get update && \
    apt-get install -y \
    gcc \
    libpq-dev \
    npm \
    iputils-ping \
    net-tools && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install \
    django \
    psycopg2-binary \
    xhtml2pdf \
    django-chartjs \
    python-bidi  # Correct package name

# Install npm packages
RUN npm install -g chart.js

# Expose port 8000 (replace with the port your app listens on)
EXPOSE 8000

# Run the Django development server on container startup
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
