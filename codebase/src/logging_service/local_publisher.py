#logging_service/local_publisher.py
import os
import logging
from concurrent import futures
import grpc
import logging_service_pb2
import logging_service_pb2_grpc

from confluent_kafka import Producer

'''
Kafka Producer: https://docs.confluent.io/kafka-clients/python/current/overview.html#ak-producer
Kafka Consumer: https://kafka.apache.org/quickstart#quickstart_consume
'''

# connect to redis database #0
# # Load Kafka server from environment variable
# kafka_server = os.getenv("KAFKA_SERVER", "localhost:9093")
# producer = Producer({'bootstrap.servers': kafka_server})
producer = Producer({'bootstrap.servers': 'localhost:9093'})
topic = 'log-channel'


# Implement the LoggingService
class LoggingServiceServicer(logging_service_pb2_grpc.LoggingServiceServicer):
  def LogOperation(self, request_iterator, context):
    try:
      for log_message in request_iterator:
        msg = f"[{log_message.timestamp}] {log_message.message}"

        # Publish to Kafka
        producer.produce(topic, msg.encode('utf-8'))
        producer.flush()

        print(f"Published message to Kafka: {msg}")

      # Send a response once the stream is complete
      return logging_service_pb2.LogResponse(confirmation="Logs processed successfully")

    except Exception as e:
      print(f"Error: {str(e)}")
      return logging_service_pb2.LogResponse(confirmation=f"Error: {str(e)}")


# Start the gRPC server
def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  logging_service_pb2_grpc.add_LoggingServiceServicer_to_server(LoggingServiceServicer(), server)
  server.add_insecure_port('[::]:50052')  # Adjust port if needed
  server.start()
  print("Logging gRPC server started on port 50052.")
  try:
    server.wait_for_termination()
  except KeyboardInterrupt:
    print("Server stopped by keyboard interrupt.")


if __name__ == '__main__':
  serve()
# produce messages
# try:
#   while True:
#     msg = f'Hello at time = {datetime.now()}'
#     producer.produce(topic, msg.encode('utf-8'))
#     producer.flush()
#     print(f"Produced message: {msg}")
#     time.sleep(1)
# except KeyboardInterrupt:
#   print('\nStopped by keyboard interrupt')
# finally:# Final flush of any remaining messages
#   producer.flush()
#   print("All pending messages sent.")
