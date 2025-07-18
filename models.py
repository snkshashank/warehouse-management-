from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='staff', nullable=False)  # Can be 'admin' or 'staff'

    shipments = db.relationship('Shipment', backref='staff', lazy=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    price = db.Column(db.Float, nullable=False)

    inventory = db.relationship('Inventory', backref='product', uselist=False, cascade="all, delete-orphan")
    shipments = db.relationship('Shipment', backref='product', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Product {self.name} - ₹{self.price}>"


class Inventory(db.Model):
    __tablename__ = 'inventory'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False, unique=True)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Inventory Product ID: {self.product_id}, Qty: {self.quantity}>"


class Shipment(db.Model):
    __tablename__ = 'shipment'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    def __repr__(self):
        return f"<Shipment Product ID: {self.product_id}, Qty: {self.quantity}, Status: {self.status}>"
