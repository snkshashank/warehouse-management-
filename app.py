from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from forms import LoginForm, RegisterForm, ProductForm, ShipmentForm
from models import db, Product, Inventory, Shipment, User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Pass%40123@localhost:3306/warehouse_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
csrf = CSRFProtect(app)
db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    try:
        product_count = Product.query.count()
        inventory_count = Inventory.query.count()
        shipment_count = Shipment.query.count()

        shipments = Shipment.query.all()
        labels = [shipment.product.name if shipment.product else "Unknown" for shipment in shipments]
        data = [shipment.quantity for shipment in shipments]

        return render_template('dashboard.html', product_count=product_count,
                               inventory_count=inventory_count,
                               shipment_count=shipment_count,
                               labels=labels, data=data)
    except Exception as e:
        print("Dashboard error:", e)
        return "Internal server error", 500

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('auth.html', form=form)

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash('Registration successful!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('register.html', form=form)

# Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))

# Products
@app.route('/product', methods=['GET', 'POST'])
@login_required
def products():
    form = ProductForm()
    search_query = request.args.get('search', '')

    if form.validate_on_submit():
        new_product = Product(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data
        )
        db.session.add(new_product)
        db.session.commit()
        flash("Product added successfully!", "success")
        return redirect(url_for('products'))

    if search_query:
        products = Product.query.filter(Product.name.ilike(f"%{search_query}%")).all()
    else:
        products = Product.query.all()

    return render_template('product.html', products=products, form=form, search_query=search_query)

@app.route('/product/delete/<int:id>')
@login_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash("Product deleted successfully.", "info")
    return redirect(url_for('products'))

# Inventory
@app.route('/inventory')
@login_required
def inventory():
    search_query = request.args.get('search', '')
    if search_query:
        items = Inventory.query.join(Product).filter(Product.name.ilike(f'%{search_query}%')).all()
    else:
        items = Inventory.query.join(Product).all()

    return render_template('inventory.html', inventory=items, search_query=search_query)

# Shipments
@app.route('/shipment', methods=['GET', 'POST'])
@login_required
def shipment():
    form = ShipmentForm()
    if form.validate_on_submit():
        shipment = Shipment(
            product_id=form.product_id.data,
            quantity=form.quantity.data,
            status=form.status.data,
            staff_id=current_user.id
        )
        db.session.add(shipment)
        db.session.commit()

        inventory = Inventory.query.filter_by(product_id=form.product_id.data).first()
        if inventory:
            inventory.quantity -= form.quantity.data
        else:
            inventory = Inventory(product_id=form.product_id.data, quantity=0 - form.quantity.data)
            db.session.add(inventory)
        db.session.commit()

        flash("Shipment recorded and inventory updated.", "success")
        return redirect(url_for('shipment'))

    shipments = Shipment.query.all()
    return render_template('shipment.html', form=form, shipments=shipments)

# Run the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
