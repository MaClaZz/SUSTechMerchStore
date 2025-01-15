# Dockerfile in ./client
FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt  # Ensure dependencies are listed in requirements.txt
CMD ["python", "ClientStub.py"]
#docker build -t local_publisher .