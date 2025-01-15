# Base image with Python 3.9 or later
FROM python:3.11

# Set environment variables (adjust based on your project)
ENV DB_USER=dncc
ENV DB_PASSWORD=dncc
ENV DB_HOST=localhost
ENV DB_PORT=2222
ENV DB_NAME=goodsstore

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the entire application code
COPY . .

# Expose the gRPC server port (change based on your server configuration)
EXPOSE 50051

# Run the gRPC service
CMD ["python", "db_service.py"]
#docker build -t db_service_image .