FROM python:3.9

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0

# Install Python dependencies
RUN pip install --upgrade pip
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

# Copy your Python scripts
COPY update_agol_layer.py /usr/src/app/update_agol_layer.py

# Set the working directory
WORKDIR /usr/src/app

# Command to run the script
CMD ["python", "update_agol_layer.py"]
