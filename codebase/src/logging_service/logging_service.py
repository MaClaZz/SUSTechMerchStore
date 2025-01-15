# # logging_service.py
# import grpc
# from concurrent import futures
# from proto import logging_service_pb2, logging_service_pb2_grpc
# from confluent_kafka import Producer
# # (a) Client-side streaming RPC to collect log messages.
#
# class LoggingService(logging_service_pb2_grpc.LoggingServiceServicer):
#     def __init__(self):
#         self.producer = Producer({"bootstrap.servers": "localhost:9092"})
#
#     def LogOperation(self, request_iterator, context):
#         for log_message in request_iterator:
#             self.producer.produce("log_topic", log_message.message)
#             self.producer.flush()
#         return logging_service_pb2.LogResponse(confirmation="Logs received")
#
# def serve():
#     server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
#     logging_service_pb2_grpc.add_LoggingServiceServicer_to_server(LoggingService(), server)
#     server.add_insecure_port("[::]:50052")
#     server.start()
#     server.wait_for_termination()
#
# if __name__ == "__main__":
#     serve()
