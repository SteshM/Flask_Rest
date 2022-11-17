from flask import Flask, request, jsonify
from flask import json
from werkzeug.exceptions import HTTPException
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
import logging
# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

#Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path. join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init na
ma = Marshmallow(app)
#ErrorHandler
@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response

   # Product Class/Model
class Product(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(100), unique=True)
  description = db.Column(db.String(200))
  price = db.Column(db.Float)
  qty = db.Column(db.Integer)

  def __init__(self,name,description,price,qty):
     self.name = name
     self.description = description
     self.price = price
     self.qty = qty

     #product schema
class ProductSchema(ma.Schema):
   class Meta:
      fields = ('id', 'name', 'description', 'price','qty')

      #init schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

     #Create a Product
@app.route('/product',methods=['POST'] )
def add_product():
   app.logger.info("This method is used to POST")
   name = request.json['name']
   app.logger.info("about to add a product with name %s", name)
   description = request.json['description']
   app.logger.info("about to add a product with description %s", description)
   price = request.json['price']
   app.logger.info("about to add a product with price %s", price)
   qty = request.json['qty']
   app.logger.info("about to add a product with qty %s", qty)

   new_product = Product(name, description,price,qty)

   db.session.add(new_product)
   db.session.commit()

   return product_schema.jsonify(new_product)

     #Get all products
@app.route('/product', methods=['GET'])
def get_products():
   app.logger.info("The method used is GET", request.method)

   all_products = Product.query.all()
   result = products_schema.dump(all_products)

   return jsonify(result)

   #Get a single product
@app.route('/product/<id>', methods=['GET'])
def get_product(id):
   product = Product.query.get(id)
   return product_schema.jsonify(product)

   #update a product
@app.route ('/product/<id>', methods=['PUT'])
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

   #delete Product
@app.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
      product = Product.query.get(id)
      db.session.delete(product)
      db.session.commit()

      return product_schema.jsonify(product)


     # Run Server
if __name__== '_main_':
  app.run(debug=True)






