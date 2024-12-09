# Use an official Python runtime as a parent image
FROM python:3.11.4-slim-buster

# Set the working directory in the container
WORKDIR /usr/src/app/

# Install system dependencies
RUN apt-get update && apt-get install -y netcat && apt-get clean

# Copy application dependencies
COPY ./app/requirements.lock /usr/src/app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.lock

# Copy the application code
COPY ./app /usr/src/app/

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/app/entrypoint.sh"]
