 # API Service:
 # (a) A Greeting API that returns a welcome message at the base URL.
 # (b) list-products and get-product operations for products.
 # (c) register, deactivate-user, get-user, update-user, login for users.
 # (d) place-order, cancel-order, get-order for orders.
 # (e) An OpenAPI specification YAML file defining the APIs above.

 # pip install Flask Flask-JWT-Extended Flask-SQLAlchemy

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost/db_name'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Change this to a secure secret
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Models
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))
    price = db.Column(db.Numeric(10, 2), nullable=False)
    slogan = db.Column(db.String(255))
    stock = db.Column(db.Integer, default=500)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

# Routes
@app.route('/')
def greet():
    return jsonify({'message': 'Welcome to the API!'})

# User routes
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    hashed_password = data['password']  # Replace with proper hashing (e.g., bcrypt)
    new_user = User(username=data['username'], password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and user.password_hash == data['password']:  # Add password hashing comparison
        access_token = create_access_token(identity=user.id)
        return jsonify({'token': access_token}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/get-user/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({'username': user.username})

# Product routes
@app.route('/products', methods=['GET'])
def list_products():
    products = Product.query.all()
    return jsonify([{'name': p.name, 'price': str(p.price)} for p in products])

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify({'name': product.name, 'price': str(product.price)})

# Order routes
@app.route('/place-order', methods=['POST'])
@jwt_required()
def place_order():
    user_id = get_jwt_identity()
    data = request.json
    # Process order logic here
    return jsonify({'message': 'Order placed successfully'}), 201

if __name__ == '__main__':
    app.run(debug=True)
