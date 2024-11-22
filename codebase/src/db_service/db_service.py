import grpc
from concurrent import futures
import time
# from models import db, Product  # Import your SQLAlchemy models
import psycopg2
from psycopg2 import pool
import os
from pprint import pprint

# Import the generated classes
import db_service_pb2
import db_service_pb2_grpc

# PostgreSQL connection pooling
db_user = os.getenv("DB_USER", "dncc")
db_password = os.getenv("DB_PASSWORD", "dncc")
db_host = os.getenv("DB_HOST", "localhost")
db_port = os.getenv("DB_PORT", "2222")
db_name = os.getenv("DB_NAME", "goodsstore")

# Create a SimpleConnectionPool for a single-threaded application
simple_pool = psycopg2.pool.SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    user=db_user,
    password=db_password,
    host=db_host,
    port=db_port,
    database=db_name
)

class DbServiceServicer(db_service_pb2_grpc.DBServiceServicer):
    def Greet(self, request, context):
        return db_service_pb2.GreetResponse(message="Welcome to the gRPC Service!")

    def Register(self, request, context):
        conn = None
        try:
            conn = simple_pool.getconn()
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO users (username, password) VALUES (%s, %s) RETURNING id;",
                    (request.username, request.password)
                )
                user_id = cursor.fetchone()[0]
                conn.commit()
                return db_service_pb2.UserResponse(id=user_id, username=request.username)
        except psycopg2.DatabaseError as e:
            context.set_details(f"Database error: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
        finally:
            if conn:
                simple_pool.putconn(conn)

    def GetUser(self, request, context):
        conn = None
        try:
            conn = simple_pool.getconn()
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE id = %s;", (request.user_id,))
                result = cursor.fetchone()
                if result:
                    return db_service_pb2.UserResponse(id=result[0], username=result[1])
                else:
                    context.set_details("User not found")
                    context.set_code(grpc.StatusCode.NOT_FOUND)
        except psycopg2.DatabaseError as e:
            context.set_details(f"Database error: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
        finally:
            if conn:
                simple_pool.putconn(conn)
    def ListProducts(self, request, context):
        conn = None
        try:
            conn = simple_pool.getconn()
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM products;")
                results = cursor.fetchall()
                products = [db_service_pb2.ProductResponse(
                    id=row[0], name=row[1], description=row[2], category=row[3],
                    price=row[4], slogan=row[5], stock=row[6]) for row in results]
            return db_service_pb2.ProductListResponse(products=products)
        except psycopg2.DatabaseError as e:
            context.set_details(f"Database error: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
        finally:
            if conn:
                simple_pool.putconn(conn)
    # return db_service_pb2.ProductListResponse(products=[
    #         db_service_pb2.ProductResponse(id=p["id"], name=p["name"], price=p["price"])
    #         for p in products_db
    #     ])
    # def GetProduct(self, request, context):
    #     product = Product.query.get(request.product_id)
    #     if product:
    #         return db_service_pb2.ProductResponse(
    #             id=product.id,
    #             name=product.name,
    #             price=str(product.price)
    #         )
    #     context.set_details('Product not found')
    #     context.set_code(grpc.StatusCode.NOT_FOUND)
    #     return db_service_pb2.ProductResponse()

    # Implement other methods similarly...

# Server setup
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
db_service_pb2_grpc.add_DBServiceServicer_to_server(DbServiceServicer(), server)
server.add_insecure_port('[::]:50051')
server.start()
print("Server started on port 50051")
server.wait_for_termination()
