import queue
import threading

import bcrypt
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import os
import time
from datetime import datetime
import sys
import sys
import os
sys.path.append(os.path.abspath("../db_service"))
sys.path.append(os.path.abspath("../logging_service"))

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../db_service')))
import grpc
import db_service_pb2
import db_service_pb2_grpc

import logging_service_pb2
import logging_service_pb2_grpc

# Connect to the gRPC LoggingService
log_channel = grpc.insecure_channel('2222:50052')  # Replace with actual host:port
log_stub = logging_service_pb2_grpc.LoggingServiceStub(log_channel)

# Thread-safe queue to hold log messages
log_queue = queue.Queue()

# Function to stream logs continuously
def stream_logs():
    def generator():
        while True:
            log_message = log_queue.get()  # Wait for a message
            if log_message is None:  # Exit signal
                break
            yield log_message

    # Start streaming to the server
    response = log_stub.LogOperation(generator())
    print("Log server response:", response.confirmation)

# Run the log streaming in a separate thread
threading.Thread(target=stream_logs, daemon=True).start()

app = Flask(__name__)
# JWT Configuration
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Use a strong secret key
jwt = JWTManager(app)
# metadata = [('authorization', f'Bearer {token}')]
# Logging middleware
@app.before_request
def log_request():
    log_message = logging_service_pb2.LogMessage(
        message=f"Incoming request: {request.method} {request.path}",
        timestamp=str(datetime.now())
    )
    log_queue.put(log_message)

@app.after_request
def log_response(response):
    log_message = logging_service_pb2.LogMessage(
        message=f"Response status: {response.status_code} for {request.method} {request.path}",
        timestamp=str(datetime.now())
    )
    log_queue.put(log_message)
    return response

# Establish a connection to the gRPC server
channel = grpc.insecure_channel('2222:50051')
stub = db_service_pb2_grpc.DBServiceStub(channel)

# Greeting Route
@app.route('/')
def greet():
    try:
        response = stub.Greet(db_service_pb2.Empty())
        return jsonify({'message': response.message}), 200
    except grpc.RpcError as e:
        return jsonify({'error': 'Product not found'}), 404

# Product Routes
@app.route('/products', methods=['GET'])
@jwt_required()  # JWT Authentication required
def list_products():
    try: # user_id = get_jwt_identity()  # Extract user ID from the JWT token
        # metadata = [('user-id', str(user_id))]  # Pass as gRPC metadata if needed
        response = stub.ListProducts(db_service_pb2.Empty())

        # response = stub.ListProducts(db_service_pb2.Empty(), metadata=metadata)
        products = [{"id": p.id, "name": p.name, "description": p.description, "category": p.category, "price": p.price, "slogan": p.slogan, "stock": p.stock} for p in response.products]
        return jsonify(products), 200
    except grpc.RpcError as e:
        return jsonify({'error': 'Product not found'}), 404

@app.route('/products/<int:product_id>', methods=['GET'])
@jwt_required()  # JWT Authentication required
def get_product(product_id):
    try:
        response = stub.GetProduct(db_service_pb2.ProductRequest(product_id=product_id))
        product = {
            "id": response.id,
            "name": response.name,
            "description": response.description,
            "category": response.category,
            "price": response.price,
            "slogan": response.slogan,
            "stock": response.stock
        }
        return jsonify(product), 200
    except grpc.RpcError as e:
        return jsonify({'error': 'Product not found'}), 404

# User Routes
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    try:
        # Check if sid and email exist in the request
        sid = data.get('sid', None)  # Default to None if not provided
        email = data.get('email', None)  # Default to None if not provided
        password = data.get('password')
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        response = stub.Register(db_service_pb2.RegisterRequest(
            sid=sid,                    # Pass sid if it exists
            username=data['username'],
            email=email,                 # Pass email if it exists
            password=password_hash
            # password=data['password'],  # Ideally, hash the password before sending
        ))
        return jsonify({
            # 'message': 'User registered successfully',
            'id': response.id,
            'sid': response.sid,
            'username': response.username,
            'email': response.email,
            # 'password': password_hash
            # 'token': access_token
        }), 200
    except grpc.RpcError as e:
        return jsonify({'error': e.details()}), 401  # Extract detailed message

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    password = data.get('password')
    # password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode()
    try:
        response = stub.LoginUser(db_service_pb2.LoginRequest(
            username=data['username'],
            password=data['password']#password_hash
        ))
        if response.token:
            return jsonify({'token': response.token}), 200
        else:
            return jsonify({'error': 'Invalid username or password'}), 401
    except grpc.RpcError as e:
        return jsonify({'error': e.details()}), 401  # Extract detailed message

@app.route('/get-user/<int:user_id>', methods=['GET'])
@jwt_required()  # JWT Authentication required
def get_user(user_id):
    # current_user_id = get_jwt_identity()  # Get user from JWT

    # Create metadata with JWT token
    token = request.headers.get('Authorization').split(" ")[1]
    metadata = [('authorization', token)]

    try:
        response = stub.GetUser(db_service_pb2.UserRequest(user_id=user_id), metadata=metadata)
        return jsonify({'id': response.id, 'username': response.username})
    except grpc.RpcError as e:
        return jsonify({'error': e.details()}), 404
@app.route('/deactivate-user/<int:user_id>', methods=['DELETE'])
@jwt_required()  # JWT Authentication required
# @jwt_required
def deactivate_user(user_id):
    try:
        response = stub.DeactivateUser(db_service_pb2.UserRequest(user_id=user_id))
        return jsonify({'message': response.message}), 200
    except grpc.RpcError as e:
        return jsonify({'error': e.details()}), 500
# Order Routes
@app.route('/update-user', methods=['PUT'])
@jwt_required()  # JWT Authentication required
def update_user():
    data = request.json
    # Check if sid and email exist in the request
    user_id = data.get('user_id', None)  # Default to None if not provided

    sid = data.get('sid', None)  # Default to None if not provided
    email = data.get('email', None)  # Default to None if not provided
    username = data.get('username')
    # password = data.get('password')
    # password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    # print(sid,email,username)
    # if not username:
    #     return jsonify({'error': 'Username is required'}), 400
    # if not email:
    #     return jsonify({'error': 'Email is required'}), 400

    # Call the gRPC UpdateUser method
    try:
        # Validate user ID
        if 'user_id' not in data:
            return jsonify({'error': 'User ID is required'}), 400

        response = stub.UpdateUser(db_service_pb2.UserUpdate(
            user_id=user_id,
            sid=sid,
            username=username,
            email=email
            # password=password_hash
        ))
        return jsonify({
            'id': response.id,
            'sid': response.sid,
            'username': response.username,
            'email': response.email
        }), 200
    except grpc.RpcError as e:
        # Check for specific gRPC error codes
        if e.code() == grpc.StatusCode.ALREADY_EXISTS:
            return jsonify({'error': e.details()}), 409  # HTTP 409 Conflict for unique violations
        elif e.code() == grpc.StatusCode.NOT_FOUND:
            return jsonify({'error': 'User not found'}), 404
        else:
            return jsonify({'error': e.details()}), 500
# Order Routes
@app.route('/place-order', methods=['POST'])
@jwt_required()  # JWT Authentication required
def place_order():
    data = request.json
    try:
        user_id = data['user_id']
        # user_id = get_jwt_identity()
        quantity = data['quantity']
        product_id = data['product_id']
        # Create metadata with JWT token
        if quantity <= 0 or quantity > 3 :
            return jsonify({'error': 'Quantity must be greater than zero & not greater than 3'}), 400

        token = request.headers.get('Authorization').split(" ")[1]
        metadata = [('authorization', token)]
        response = stub.PlaceOrder(db_service_pb2.PlaceOrderRequest(user_id=user_id, product_id=product_id,quantity=quantity),metadata=metadata)
        return jsonify({'message': response.message}), 200
    except grpc.RpcError as e:
        return jsonify({'error': e.details()}), 500
@app.route('/get-order/<int:order_id>', methods=['GET'])
@jwt_required()  # JWT Authentication required
def get_order(order_id):
    data = request.json
    # order_id = data.get('order_id', None)  # Default to None if not provided
    user_id = data.get('user_id', None)  # Default to None if not provided
    # product_id = data.get('product_id', None)  # Default to None if not provided

    # Create metadata with JWT token
    token = request.headers.get('Authorization').split(" ")[1]
    metadata = [('authorization', token)]
    try:
        # if not user_id or not product_id:
        #     return jsonify({'message': 'Missing required parameters: user_id or product_id'}), 400
        # request = db_service_pb2.OrderRequest(order_id=order_id)
        # print(request)
        response = stub.GetOrder(db_service_pb2.OrderRequest(order_id=order_id),metadata=metadata)
        # print(response)

        if response.order_id == 0:
            return jsonify({'message': 'Order not found'}), 404

        return jsonify({
            'order_id': response.order_id,
            'user_id': response.user_id,
            'product_id': response.product_id,
            'quantity': response.quantity,
            'total_price': response.total_price
        }), 200
    except grpc.RpcError as e:
        return jsonify({'error': e.details()}), 404
@app.route('/cancel-order/<int:order_id>', methods=['DELETE'])
@jwt_required()  # JWT Authentication required
# @jwt_required
def cancel_order(order_id):
    try:
        response = stub.CancelOrder(db_service_pb2.OrderRequest(order_id=order_id))
        return jsonify({'message': response.message}), 200
    except grpc.RpcError as e:
        return jsonify({'error': e.details()}), 404
@app.route('/update-order', methods=['PUT'])
@jwt_required()  # JWT Authentication required
def update_order():
    data = request.json
    # Check if sid and email exist in the request
    order_id = data.get('order_id', None)  # Default to None if not provided
    user_id = data.get('user_id', None)  # Default to None if not provided
    product_id = data.get('product_id', None)  # Default to None if not provided
    quantity = data.get('quantity', None)  # Default to None if not provided

    # Call the gRPC UpdateUser method
    try:
        # Validate user ID
        if 'user_id' not in data:
            return jsonify({'error': 'User ID is required'}), 400
        if not product_id:
            return jsonify({'error': 'Product ID is required'}), 400
        # if not quantity:
        #     return jsonify({'error': 'Email is required'}), 400
        response = stub.UpdateOrder(db_service_pb2.OrderUpdate(
            order_id=order_id,
            user_id=user_id,
            product_id=product_id,
            quantity=quantity
        ))
        return jsonify({
            'order_id': response.order_id,
            'user_id': response.user_id,
            'product_id': response.product_id,
            'quantity': response.quantity,
            'total_price': response.total_price
        }), 200
    except grpc.RpcError as e:
        return jsonify({'error': e.details()}), 500

if __name__ == '__main__':
    app.run(debug=True)
