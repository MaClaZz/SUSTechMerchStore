# psycopg2_pool.py
import grpc
from concurrent import futures
from proto import db_service_pb2, db_service_pb2_grpc
import psycopg2
from psycopg2 import pool

class DBService(db_service_pb2_grpc.DBServiceServicer):
    def __init__(self):
        self.connection_pool = psycopg2.pool.SimpleConnectionPool(1, 10, user="username",
                                                                  password="password",
                                                                  host="localhost",
                                                                  port="5432",
                                                                  database="merch_db")
    def CreateUser(self, request, context):
        conn = self.connection_pool.getconn()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s) RETURNING id;",
                       (request.username, request.password_hash))
        conn.commit()
        cursor.close()
        self.connection_pool.putconn(conn)
        return db_service_pb2.UserResponse(message="User created")
# (b) list-products and get-product operations for products.
# (c) register, deactivate-user, get-user, update-user, login for users.
# (d) place-order, cancel-order, get-order for orders.
    def CreateProduct(self, request, context):
        return;
    def CreateOrder(self, request, context):
        return;

    def ReadUser(self, request, context):
        return;
    def ReadUser(self, request, context):
        return;
    def ReadUser(self, request, context):
        return;

    def UpdateUser(self, request, context):
        return;
    def UpdateUser(self, request, context):
        return;
    def UpdateUser(self, request, context):
        return;

    def DeleteUser(self, request, context):
        return;
    def DeleteUser(self, request, context):
        return;
    def DeleteUser(self, request, context):
        return;

# Start gRPC Server
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    db_service_pb2_grpc.add_DBServiceServicer_to_server(DBService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
