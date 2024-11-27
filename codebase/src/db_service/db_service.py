import bcrypt
import grpc
from concurrent import futures
import time
# from models import db, Product  # Import your SQLAlchemy models
import psycopg2
from flask_jwt_extended import create_access_token
from psycopg2 import pool
import os
from pprint import pprint

# Import the generated classes
import db_service_pb2
import db_service_pb2_grpc
from codebase.src.api_service.ClientStub import app

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
    def GetProduct(self, request, context):
        conn = None
        try:
            conn = simple_pool.getconn()
            # print(request.product_id)
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM products WHERE id = %s;", (request.product_id,))
                result = cursor.fetchone()
                if result:
                    return db_service_pb2.ProductResponse(
                    id=result[0], name=result[1], description=result[2], category=result[3],
                    price=result[4], slogan=result[5], stock=result[6])
                else:
                    context.set_details("Product not found")
                    context.set_code(grpc.StatusCode.NOT_FOUND)
        except psycopg2.DatabaseError as e:
            context.set_details(f"Database error: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
        finally:
            if conn:
                simple_pool.putconn(conn)

    def Register(self, request, context):
        conn = None
        try:
            conn = simple_pool.getconn()
            with conn.cursor() as cursor:
                # Hash the password
                # password_hash = bcrypt.hashpw(request.password.encode('utf-8'), bcrypt.gensalt())
                cursor.execute(
                    "INSERT INTO users (sid, username, email, password_hash) "
                    "VALUES (%s, %s, %s, %s) RETURNING id;",
                    (request.sid, request.username, request.email, request.password)
                )
                user_id = cursor.fetchone()[0]
                conn.commit()
                return db_service_pb2.UserResponse(id=user_id, sid=request.sid, username=request.username, email=request.email)
        except psycopg2.DatabaseError as e:
            context.set_details(f"Database error: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
        finally:
            if conn:
                simple_pool.putconn(conn)

    def LoginUser(self, request, context):
        conn = None
        try:
            conn = simple_pool.getconn()
            with conn.cursor() as cursor:
                # Check if the user exists
                cursor.execute("SELECT id, password_hash FROM users WHERE username = %s;", (request.username,))
                user = cursor.fetchone()
                if user is None:
                    context.set_details("Invalid username or password.")
                    context.set_code(grpc.StatusCode.UNAUTHENTICATED)
                    return db_service_pb2.TokenResponse(token="")
                # Verify the password
                user_id, stored_password_hash = user
                # print(bcrypt.checkpw(request.password.encode(), stored_password_hash.encode()))
                if not bcrypt.checkpw(request.password.encode(), stored_password_hash.encode()):
                    context.set_details("Invalid username or password.")
                    context.set_code(grpc.StatusCode.UNAUTHENTICATED)
                    return db_service_pb2.TokenResponse(token="")
                # Create a JWT token
                # Create a JWT token within Flask app context
                with app.app_context():
                    access_token = create_access_token(identity=request.username)
                    # print(access_token)
                # Return the token
                return db_service_pb2.TokenResponse(token=access_token)
        except psycopg2.DatabaseError as e:
            context.set_details(f"Database error: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            return db_service_pb2.TokenResponse(token="")
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

    def DeactivateUser(self, request, context):
        conn = None
        try:
            conn = simple_pool.getconn()
            cursor = conn.cursor()
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM users WHERE id = %s", (request.user_id,))
                conn.commit()
                return db_service_pb2.GenericResponse(message="User deactivated")#status="Success",
        except Exception as e:
            conn.rollback()
            return db_service_pb2.GenericResponse(message=str(e))#status="Error",
        finally:
            cursor.close()
            conn.close()

    # Implement other methods similarly...

    def PlaceOrder(self, request, context):
        # print(f"Placing order for user {request.user_id}, product {request.product_name}")
        conn = None
        try:
            conn = simple_pool.getconn()
            cursor = conn.cursor()
            cursor.execute("SELECT price FROM products WHERE id = %s", (request.product_id,))
            product = cursor.fetchone()
            if not product:
                return db_service_pb2.GenericResponse(message="Error: Product not found")#status="Error",

            total_price = product[0] * request.quantity
            print(request.user_id, request.product_id, request.quantity, total_price)
            # Insert into orders table
            cursor.execute("""
                            INSERT INTO orders (user_id, product_id, quantity, total_price)
                            VALUES (%s, %s, %s, %s)
                        """, (request.user_id, request.product_id, request.quantity, total_price))

            conn.commit()
            return db_service_pb2.GenericResponse(message="Order placed successfully")
        except Exception as e:
            conn.rollback()
            return db_service_pb2.GenericResponse(message=str(e))
        finally:
            cursor.close()
            conn.close()
# Server setup
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
db_service_pb2_grpc.add_DBServiceServicer_to_server(DbServiceServicer(), server)
server.add_insecure_port('[::]:50051')
server.start()
print("Server started on port 50051")
server.wait_for_termination()
