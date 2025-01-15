# #db_service/local_manager.py
# import os
# import psycopg2
# from psycopg2 import pool   # this line is oddly necessary
# from pprint import pprint
#
# """
# Connection pooling: https://www.psycopg.org/docs/pool.html
# Connection: https://www.psycopg.org/docs/connection.html
# Cursor: https://www.psycopg.org/docs/cursor.html
# """
# # Load sensitive data from environment variables
# db_user = os.getenv("DB_USER", "dncc")
# db_password = os.getenv("DB_PASSWORD", "dncc")
# db_host = os.getenv("DB_HOST", "localhost")
# db_port = os.getenv("DB_PORT", "2222")
# db_name = os.getenv("DB_NAME", "goodsstore")
#
# # Create a SimpleConnectionPool for a single-threaded application
# simple_pool = psycopg2.pool.SimpleConnectionPool(
#   minconn=1,
#   maxconn=10,
#   # user="dncc",
#   user=db_user,
#   # maybe password need to be read from environment variable for security issue
#   password=db_password,
#   host=db_host,
#   # password="dncc",
#   # host="localhost",
#   port="2222",
#   # port=db_port,
#   database=db_name
#   # database="goodsstore"
# )
#
# # Single-threaded usage of connections
# try:
#     # Get a connection from the pool
#   conn = simple_pool.getconn()
#
#   # Perform a database operation
#   with conn.cursor() as cursor:
#     cursor.execute("SELECT * FROM products;")
#     results = cursor.fetchall()
#     pprint(results)
#     # Commit only for INSERT/UPDATE/DELETE operations.
#     # cursor.execute("INSERT INTO products (name, stock, price) VALUES (%s, %s, %s) RETURNING id", ("SUSTech Pixel Map", 300, 3.99))
#     # results = cursor.fetchone()
#     # pprint(results)
#     # conn.commit()
#     # Rollback when sth is wrong.
# except psycopg2.DatabaseError as e:
#   print(f"Database error: {e}")
#   conn.rollback()
#
#     # conn.rollback()
# finally:
#   if conn:
#     # Return the connection to the pool
#     simple_pool.putconn(conn)
#
#   # Closing all connections in the pool
#   simple_pool.closeall()
