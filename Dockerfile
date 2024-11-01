# Use the official Python image
FROM python:3-slim

# Set the working directory
WORKDIR /app

# Copy the producer and consumer folders into the image
COPY ./producer /app/producer
COPY ./consumer /app/consumer
COPY ./docker-compose.yml /app

# Install required libraries for producer and consumer
RUN pip install kafka-python

# Set the entrypoint for the container
CMD ["tail", "-f", "/dev/null"]  # Keep the container running
