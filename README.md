                                                  📦 Warehouse Management (Flask)


A web-based Warehouse Management System (WMS) built using Flask, designed to manage products, inventory, and shipment tracking with authentication and role-based access.


🚀 Features - 

1. User Authentication

Register/Login with secure password hashing

Role-based access: Admin and Staff


2. Dashboard

Overview of total products, inventory, and shipments

Visual summary using shipment data


3. Product Management

Add, search, and delete products

Each product has a name, description, and price


4. Inventory Management

Track product quantities in stock

Automatically adjusts on shipment creation


5. Shipment Tracking

Record outgoing shipments

Track status: Pending, Shipped, Delivered

Automatically deducts from inventory



🧩 Tech Stack - 

Backend: Python, Flask

ORM: SQLAlchemy

Database: MySQL (via pymysql)

Authentication: Flask-Login

Forms & Validation: Flask-WTF, WTForms

UI: HTML templates rendered using Jinja2




🛠️ Project Structure -  

├── app.py             
├── models.py         
├── forms.py          
├── templates/     
└── static/  



🔐 Roles - 

Admin: Full access to the system

Staff: Limited to inventory and shipment actions




📝 Setup Instructions -

1. Configure Database

Update the MySQL connection string in app.py:
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Pass@123@localhost:3306/warehouse_db'


2. Run the app
   
python app.py


3. Access
   
Open your browser and go to http://127.0.0.1:5000



Security Notes - 

CSRF protection is enabled using Flask-WTF

Passwords are securely hashed using Werkzeug

Input validation is handled via WTForms validators




Future Improvements (Optional) - 

Add unit tests

Add REST API support

Export inventory/shipment data to CSV

Implement email notifications
