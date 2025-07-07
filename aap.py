from flask import Flask, request, jsonify, send_from_directory
import sqlite3
import os

app = Flask(__name__, template_folder='templates') # Serve HTML templates from 'templates' folder
DATABASE = 'inventory.db' # SQLite database file

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row # Allows accessing columns by name (e.g., row['name'])
    return conn

# --- Frontend Routes (Serving HTML, CSS, JS) ---

@app.route('/')
def serve_index():
    """Serves the main index.html page."""
    return send_from_directory(app.template_folder, 'index.html')

@app.route('/template/<path:filename>')
def serve_template(filename):
    """Serves HTML templates from the 'templates' folder."""
    return send_from_directory(app.template_folder, filename)

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serves static files (CSS, JS, images) from the 'static' folder."""
    # Ensure the path is correct for static files
    return send_from_directory('static', filename)

# --- API Endpoints for Data Management ---

# Categories API
@app.route('/api/categories', methods=['GET', 'POST'])
def categories_api():
    conn = get_db_connection()
    cursor = conn.cursor()
    if request.method == 'GET':
        categories = cursor.execute('SELECT * FROM categories').fetchall()
        return jsonify([dict(row) for row in categories])
    elif request.method == 'POST':
        data = request.json
        name = data.get('name')
        description = data.get('description')
        if not name:
            return jsonify({'error': 'Category name is required'}), 400
        try:
            cursor.execute('INSERT INTO categories (name, description) VALUES (?, ?)', (name, description))
            conn.commit()
            return jsonify({'message': 'Category added successfully', 'id': cursor.lastrowid}), 201
        except sqlite3.IntegrityError:
            return jsonify({'error': 'Category with this name already exists'}), 409
        finally:
            conn.close()
            # Login API
            @app.route('/api/login', methods=['POST'])
            def login_api():
                data = request.json
                email = data.get('email')
                role = data.get('role')  # 'staff' or 'manager'
                if not all([email, role]):
                    return jsonify({'error': 'Missing login data'}), 400

                conn = get_db_connection()
                cursor = conn.cursor()
                table = None
                if role == 'staff':
                    table = 'staff'
                elif role == 'manager':
                    table = 'managers'
                else:
                    conn.close()
                    return jsonify({'error': 'Invalid role'}), 400

                user = cursor.execute(f'SELECT * FROM {table} WHERE email = ?', (email,)).fetchone()
                conn.close()
                if user:
                    return jsonify({'message': 'Login successful', 'user': dict(user)}), 200
                else:
                    return jsonify({'error': 'Invalid email or role'}), 401
# Products API
@app.route('/api/products', methods=['GET', 'POST'])
def products_api():
    conn = get_db_connection()
    cursor = conn.cursor()
    if request.method == 'GET':
        # Join with categories table to get category name
        products = cursor.execute('SELECT p.*, c.name as category_name FROM products p JOIN categories c ON p.category_id = c.id').fetchall()
        return jsonify([dict(row) for row in products])
    elif request.method == 'POST':
        data = request.json
        name = data.get('name')
        category_name = data.get('category') # Frontend sends category name
        price = data.get('price')
        quantity = data.get('qty')

        if not all([name, category_name, price, quantity is not None]):
            return jsonify({'error': 'Missing product data'}), 400

        try:
            # Get category_id from category_name
            category = cursor.execute('SELECT id FROM categories WHERE name = ?', (category_name,)).fetchone()
            if not category:
                return jsonify({'error': f'Category "{category_name}" not found'}), 404
            category_id = category['id']

            cursor.execute('INSERT INTO products (name, category_id, price, quantity) VALUES (?, ?, ?, ?)',
                           (name, category_id, price, quantity))
            conn.commit()
            return jsonify({'message': 'Product added successfully', 'id': cursor.lastrowid}), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            conn.close()

# Staff API
@app.route('/api/staff', methods=['GET', 'POST'])
def staff_api():
    conn = get_db_connection()
    cursor = conn.cursor()
    if request.method == 'GET':
        staff = cursor.execute('SELECT * FROM staff').fetchall()
        return jsonify([dict(row) for row in staff])
    elif request.method == 'POST':
        data = request.json
        name = data.get('name')
        position = data.get('position')
        email = data.get('email')
        if not all([name, position, email]):
            return jsonify({'error': 'Missing staff data'}), 400
        try:
            cursor.execute('INSERT INTO staff (name, position, email) VALUES (?, ?, ?)', (name, position, email))
            conn.commit()
            return jsonify({'message': 'Staff added successfully', 'id': cursor.lastrowid}), 201
        except sqlite3.IntegrityError:
            return jsonify({'error': 'Staff with this email already exists'}), 409
        finally:
            conn.close()

# Managers API
@app.route('/api/managers', methods=['GET', 'POST'])
def managers_api():
    conn = get_db_connection()
    cursor = conn.cursor()
    if request.method == 'GET':
        managers = cursor.execute('SELECT * FROM managers').fetchall()
        return jsonify([dict(row) for row in managers])
    elif request.method == 'POST':
        data = request.json
        name = data.get('name')
        department = data.get('department')
        email = data.get('email')
        if not all([name, department, email]):
            return jsonify({'error': 'Missing manager data'}), 400
        try:
            cursor.execute('INSERT INTO managers (name, department, email) VALUES (?, ?, ?)', (name, department, email))
            conn.commit()
            return jsonify({'message': 'Manager added successfully', 'id': cursor.lastrowid}), 201
        except sqlite3.IntegrityError:
            return jsonify({'error': 'Manager with this email already exists'}), 409
        finally:
            conn.close()

# Customers API
@app.route('/api/customers', methods=['GET', 'POST'])
def customers_api():
    conn = get_db_connection()
    cursor = conn.cursor()
    if request.method == 'GET':
        customers = cursor.execute('SELECT * FROM customers').fetchall()
        return jsonify([dict(row) for row in customers])
    elif request.method == 'POST':
        data = request.json
        name = data.get('name')
        phone = data.get('phone')
        email = data.get('email')
        if not all([name, phone, email]):
            return jsonify({'error': 'Missing customer data'}), 400
        try:
            cursor.execute('INSERT INTO customers (name, phone, email) VALUES (?, ?, ?)', (name, phone, email))
            conn.commit()
            return jsonify({'message': 'Customer added successfully', 'id': cursor.lastrowid}), 201
        except sqlite3.IntegrityError:
            return jsonify({'error': 'Customer with this email already exists'}), 409
        finally:
            conn.close()

# --- Database Initialization ---

def create_tables():
    """Creates necessary tables in the SQLite database if they don't exist."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category_id INTEGER NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL,
            FOREIGN KEY (category_id) REFERENCES categories(id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS staff (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            position TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS managers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_initial_data():
    """Adds some initial data to the categories table if it's empty."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    # Add some initial categories if not present
    categories = [
        ('Electronics', 'Electronic items'),
        ('Clothing', 'Apparel and garments'),
        ('Groceries', 'Daily grocery items')
    ]
    for name, desc in categories:
        try:
            cursor.execute('INSERT INTO categories (name, description) VALUES (?, ?)', (name, desc))
        except sqlite3.IntegrityError:
            # Category already exists, ignore
            pass
    conn.commit()
    conn.close()

if __name__ == '__main__':
    # Ensure the database and initial data are set up before running the app
    create_tables()
    add_initial_data()
    app.run(debug=True, port=5500) # Run on port 5500 to match your frontend links
