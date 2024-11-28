import bcrypt
import grpc
from concurrent import futures
import time
# from models import db, Product  # Import your SQLAlchemy models
import psycopg2
from psycopg2 import errors

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
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM users WHERE id = %s", (request.user_id,))
                conn.commit()
                return db_service_pb2.GenericResponse(message="User deactivated")#status="Success",
        except Exception as e:
            conn.rollback()
            return db_service_pb2.GenericResponse(message=str(e))#status="Error",
        finally:
            if conn:
                simple_pool.putconn(conn)
    def UpdateUser(self, request, context):
        print(f"Updating user")
        conn = None
        try:
            conn = simple_pool.getconn()
            with conn.cursor() as cursor:
                # Update fields dynamically
                updates = []
                params = []

                if request.sid:
                    updates.append("sid = %s")
                    params.append(request.sid)
                if request.username:
                    updates.append("username = %s")
                    params.append(request.username)

                if request.email:
                    updates.append("email = %s")
                    params.append(request.email)

                # if request.password:
                #     password_hash = bcrypt.hashpw(request.password.encode('utf-8'), bcrypt.gensalt())
                #     updates.append("password_hash = %s")
                #     params.append(password_hash.decode())

                if not updates:
                    context.set_details("No fields to update")
                    context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                    return db_service_pb2.UserResponse()
                params.append(request.user_id)
                print(updates)
                update_query = f"UPDATE users SET {', '.join(updates)} WHERE id = %s RETURNING id, sid, username, email"
                cursor.execute(update_query, tuple(params))
                print(update_query, tuple(params))

                updated_user = cursor.fetchone()

                if updated_user:
                    conn.commit()
                    return db_service_pb2.UserResponse(
                        id=updated_user[0], sid=updated_user[1],
                        username=updated_user[2], email=updated_user[3]
                    )
                else:
                    context.set_details("User not found")
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    return db_service_pb2.UserResponse()


        except psycopg2.errors.UniqueViolation as e:
            conn.rollback()
            # Custom error message for unique constraint violation
            error_detail = str(e).split("\n")[0]  # Get the first line of the error
            if "users_sid_key" in error_detail:
                context.set_details("SID already exists. Please choose a different SID.")
            else:
                context.set_details("Unique constraint violation occurred.")
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
        except psycopg2.DatabaseError as e:
            conn.rollback()
            context.set_details(f"Database error: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
        finally:
            if conn:
                simple_pool.putconn(conn)

    # Implement other methods similarly...
    # Server-side gRPC method for getting order details
    def GetOrder(self, request, context):
        # print(f"Getting order for user")
        conn = None
        try:
            conn = simple_pool.getconn()
            with conn.cursor() as cursor:
                # Fetch the order details
                cursor.execute("SELECT * FROM orders WHERE id = %s;", (request.order_id,))
                order = cursor.fetchone()
                print(order)
                if order:
                    return db_service_pb2.OrderResponse(order_id=order[0],
                    user_id=order[1],
                    product_id=order[2],
                    quantity=order[3],
                    total_price=order[4])
                else:
                    context.set_details("Order not found")
                    context.set_code(grpc.StatusCode.NOT_FOUND)
        except psycopg2.DatabaseError as e:
            context.set_details(f"Database error: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
        finally:
            if conn:
                simple_pool.putconn(conn)


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
            # Extract relevant information from the error message
            if 'violates check constraint' in str(e):
                return db_service_pb2.GenericResponse(message="Order failed: Invalid quantity or data.")
            return db_service_pb2.GenericResponse(message="Database error occurred.")
            # return db_service_pb2.GenericResponse(message=str(e))
        finally:
            if conn:
                simple_pool.putconn(conn)

    def CancelOrder(self, request, context):
        conn = None
        try:
            conn = simple_pool.getconn()
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM orders WHERE id = %s", (request.order_id,))
                conn.commit()
                return db_service_pb2.GenericResponse(message="Order deactivated")#status="Success",
        except Exception as e:
            conn.rollback()
            return db_service_pb2.GenericResponse(message="Error canceling order: " + str(e).split("\n")[0])
            # return db_service_pb2.GenericResponse(message=str(e))#status="Error",
        finally:
            if conn:
                simple_pool.putconn(conn)
    def UpdateOrder(self, request, context):
        print(f"Updating order for user")
        conn = None
        try:
            conn = simple_pool.getconn()
            cursor = conn.cursor()
            # Update fields dynamically
            updates = []
            params = []
            # Check if the product,user_id still the sameorder exists
            cursor.execute("SELECT * FROM orders WHERE id = %s", (request.order_id,))
            ori_order = cursor.fetchone()
            if not ori_order:
                # return db_service_pb2.GenericResponse(message="Error: Order not found")
                context.set_details("Error: Order not found")
                context.set_code(grpc.StatusCode.NOT_FOUND)
                return db_service_pb2.OrderResponse()
            # # Ensure the order exists first
            # cursor.execute("SELECT product_id FROM orders WHERE id = %s", (request.order_id,))
            # order = cursor.fetchone()
            # if not order:
            #     return db_service_pb2.GenericResponse(message="Error: Order not found")
            if request.quantity:
                updates.append("quantity = %s")
                params.append(request.quantity)
                # Validate quantity
                if request.quantity <= 0 or request.quantity > 3:
                    # print(request.quantity)
                    # return db_service_pb2.GenericResponse(message="Error: Quantity must be between 1 and 3")
                    context.set_details("Error: Quantity must be between 1 and 3")
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    return db_service_pb2.OrderResponse()
            if request.product_id:
                # print("have request.product_id")
                if request.product_id!=ori_order[2]:
                    updates.append("product_id = %s")
                    params.append(request.product_id)
                # Fetch the product price for recalculating total_price
                cursor.execute("SELECT price FROM products WHERE id = %s", (request.product_id,))
                product = cursor.fetchone()
                # print(float(product[0]))
                if not product:
                    # return db_service_pb2.GenericResponse(message="Error: Product associated with order not found")
                    context.set_details("Error: Product associated with order not found")
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    return db_service_pb2.OrderResponse()
                # Calculate new total price
                total_price = float(product[0]) * request.quantity
                updates.append("total_price = %s")
                params.append(total_price)
                # print(updates)
                # print(params)
            else:
                #Check if the order exists
                cursor.execute("SELECT product_id FROM orders WHERE id = %s", (request.order_id,))
                order = cursor.fetchone()
                # print(order)
                if not order:
                    # return db_service_pb2.GenericResponse(message="Error: Order not found")
                    context.set_details("Error: Order not found")
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    return db_service_pb2.OrderResponse()
                # Fetch the product price for recalculating total_price
                cursor.execute("SELECT price FROM products WHERE id = %s", (order[0],))
                product = cursor.fetchone()
                # print(order)
                if not print:
                    # return db_service_pb2.GenericResponse(message="Error: Product associated with order not found")
                    context.set_details("Error: Product associated with order not found")
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    return db_service_pb2.OrderResponse()
                # Calculate new total price
                total_price = float(product[0]) * request.quantity
                updates.append("total_price = %s")
                params.append(total_price)


            if request.user_id != ori_order[1]:
                # return db_service_pb2.GenericResponse(message="Error: can't change user_id")
                context.set_details("Error: can't change user_id")
                context.set_code(grpc.StatusCode.NOT_FOUND)
                return db_service_pb2.OrderResponse()

            params.append(request.order_id)
            print(params)
            # Update the order in the database
            update_query = f"UPDATE orders SET {', '.join(updates)} WHERE id = %s RETURNING id, user_id, product_id, quantity, total_price"
            cursor.execute(update_query, tuple(params))
            print(update_query, tuple(params))

            updated_order = cursor.fetchone()
            print(updated_order)
            if updated_order:
                conn.commit()
                return db_service_pb2.OrderResponse(
                    order_id=updated_order[0],
                    user_id=updated_order[1],
                    product_id=updated_order[2],
                    quantity=updated_order[3],
                    total_price=updated_order[4])
            else:
                context.set_details("Order not found")
                context.set_code(grpc.StatusCode.NOT_FOUND)
                return db_service_pb2.OrderResponse()
            # conn.commit()
            # return db_service_pb2.GenericResponse(message="Order updated successfully")
        except psycopg2.errors.UniqueViolation as e:
                conn.rollback()
                # Custom error message for unique constraint violation
                error_detail = str(e).split("\n")[0]  # Get the first line of the error
                if "users_sid_key" in error_detail:
                    context.set_details("SID already exists. Please choose a different SID.")
                else:
                    context.set_details("Unique constraint violation occurred.")
                context.set_code(grpc.StatusCode.ALREADY_EXISTS)
        except psycopg2.DatabaseError as e:
            conn.rollback()
            context.set_details(f"Database error: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
        finally:
            if conn:
                simple_pool.putconn(conn)

# Server setup
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
db_service_pb2_grpc.add_DBServiceServicer_to_server(DbServiceServicer(), server)
server.add_insecure_port('[::]:50051')
server.start()
print("Server started on port 50051")
server.wait_for_termination()
