# Base image: Python with a compatible version
FROM python:3.11

# Set working directory
WORKDIR /app

# Install dependencies
# For grpc and Kafka producer client
COPY requirements.txt .

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the script and protobuf files
COPY local_publisher.py .
COPY logging_service_pb2.py .
COPY logging_service_pb2_grpc.py .

# Set environment variables if needed (e.g., Kafka server address)
# ENV KAFKA_SERVER=kafka:9093

# Expose the gRPC server port
EXPOSE 50052

# Command to run the service
CMD ["python", "local_publisher.py"]
#docker build -t local_publisher .