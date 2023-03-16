from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
import os 

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

# Product Class/Model
class Product(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), unique=True)
  description = db.Column(db.String(200))
  price = db.Column(db.Float)
  qty = db.Column(db.Integer)

  def __init__(self, name, description, price, qty):
    self.name = name
    self.description = description
    self.price = price
    self.qty = qty

# Product Schema
class ProductSchema(ma.Schema):
  class Meta:
    fields = ('id', 'name', 'description', 'price', 'qty')

# Init schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)




#User Model
class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(50), unique=True)
  email = db.Column(db.String(100), unique=True)
  password = db.Column(db.String(100))

  def __init__(self, username, email, password):
    self.username = username
    self.email = email
    self.password = password

class UserSchema(ma.Schema):
  class Meta:
    fields = ('id', 'username', 'email', 'password')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@app.before_first_request
def create_tables():
    db.create_all()
# Create a Product
@app.route('/product', methods=['POST'])
def add_product():
  name = request.json['name']
  description = request.json['description']
  price = request.json['price']
  qty = request.json['qty']

  new_product = Product(name, description, price, qty)

  db.session.add(new_product)
  db.session.commit()

  return product_schema.jsonify(new_product)

# Get All Products
@app.route('/product', methods=['GET'])
def get_products():
  all_products = Product.query.all()
  result = products_schema.dump(all_products)
  return jsonify(result)

# Get Single Products
@app.route('/product/<id>', methods=['GET'])
def get_product(id):
  product = Product.query.get(id)
  return product_schema.jsonify(product)

# Update a Product
@app.route('/product/<id>', methods=['PUT'])
def update_product(id):
  product = Product.query.get(id)

  name = request.json['name']
  description = request.json['description']
  price = request.json['price']
  qty = request.json['qty']

  product.name = name
  product.description = description
  product.price = price
  product.qty = qty

  db.session.commit()

  return product_schema.jsonify(product)

# Delete Product
@app.route('/product/<id>', methods=['DELETE'])
def delete_product(id):  
  product = Product.query.get(id)
  db.session.delete(product)
  db.session.commit()

  return product_schema.jsonify(product)


#user Routes
@app.route('/users', methods=['POST'])
def add_user():
  username = request.json['username']
  email = request.json['email']
  password = request.json['password']

  new_user = User(username, email, password)

  db.session.add(new_user)
  db.session.commit()

  return user_schema.jsonify(new_user)

# Get All Users
@app.route('/users', methods=['GET'])
def get_users():
  all_users = User.query.all()
  result = users_schema.dump(all_users)
  return jsonify(result)

# Get Single User
@app.route('/users/<id>', methods=['GET'])
def get_user(id):
  user = User.query.get(id)
  return user_schema.jsonify(user)

# Update a User
@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
  user = User.query.get(id)

  username = request.json['username']
  email = request.json['email']
  password = request.json['password']

  user.username = username
  user.email = email
  user.password = password

  db.session.commit()

  return user_schema.jsonify(user)

# Delete User
@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):  
  user = User.query.get(id)
  db.session.delete(user)
  db.session.commit()

  return user_schema.jsonify(user)

# Run Server
if __name__ == '__main__':
  app.run(debug=True)