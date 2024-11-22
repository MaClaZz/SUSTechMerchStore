from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import os
import sys
import sys
import os
sys.path.append(os.path.abspath("../db_service"))

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../db_service')))
import grpc
import db_service_pb2
import db_service_pb2_grpc


app = Flask(__name__)
# JWT Configuration
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Use a strong secret key
jwt = JWTManager(app)
# metadata = [('authorization', f'Bearer {token}')]

# Establish a connection to the gRPC server
channel = grpc.insecure_channel('localhost:50051')
stub = db_service_pb2_grpc.DBServiceStub(channel)

# Greeting Route
@app.route('/')
def greet():
    response = stub.Greet(db_service_pb2.Empty())
    return jsonify({'message': response.message})

# Product Routes
@app.route('/products', methods=['GET'])
@jwt_required()  # JWT Authentication required
def list_products():
    user_id = get_jwt_identity()  # Extract user ID from the JWT token
    # metadata = [('user-id', str(user_id))]  # Pass as gRPC metadata if needed
    response = stub.ListProducts(db_service_pb2.Empty(user_id=user_id))

    # response = stub.ListProducts(db_service_pb2.Empty(), metadata=metadata)
    products = [{"id": p.id, "name": p.name, "price": p.price} for p in response.products]
    return jsonify(products)

@app.route('/products/<int:product_id>', methods=['GET'])
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
        return jsonify(product)
    except grpc.RpcError as e:
        return jsonify({'error': 'Product not found'}), 404

# User Routes
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    response = stub.RegisterUser(db_service_pb2.RegisterRequest(
        username=data['username'],
        password=data['password']  # Ideally, hash the password before sending
    ))
    return jsonify({'message': 'User registered successfully', 'id': response.id})

@app.route('/get-user/<int:user_id>', methods=['GET'])
@jwt_required()  # JWT Authentication required
def get_user(user_id):
    try:
        response = stub.GetUser(db_service_pb2.UserRequest(user_id=user_id))
        return jsonify({'id': response.id, 'username': response.username})
    except grpc.RpcError:
        return jsonify({'error': 'User not found'}), 404

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    try:
        response = stub.LoginUser(db_service_pb2.LoginRequest(
            username=data['username'],
            password=data['password']
        ))
        access_token = create_access_token(identity=response.id)
        return jsonify({'token': access_token})
    except grpc.RpcError:
        return jsonify({'error': 'Invalid credentials'}), 401

# Order Routes
@app.route('/place-order', methods=['POST'])
def place_order():
    data = request.json
    # user_id = data['user_id']
    user_id = get_jwt_identity()
    product_id = data['product_id']
    response = stub.PlaceOrder(db_service_pb2.OrderRequest(user_id=user_id, product_id=product_id))
    return jsonify({'message': response.message})

if __name__ == '__main__':
    app.run(debug=True)
