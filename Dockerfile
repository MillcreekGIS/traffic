# Use a lighter base image
FROM python:3.9-slim

# Install required packages
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    krb5-user \
    libkrb5-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Copy the requirements file and install dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Install arcgis separately to manage its large number of dependencies
RUN pip install --no-cache-dir arcgis

# Copy the rest of the application code
COPY . /app

# Set the working directory
WORKDIR /app

# Set the entry point
CMD ["python", "main.py"]
