import sqlite3
import os
from datetime import datetime

DATABASE_PATH = 'store.db'

def init_db():
    """Initialize the database with basic tables"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Products table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            category TEXT NOT NULL,
            image_url TEXT,
            featured BOOLEAN DEFAULT 0,
            in_stock BOOLEAN DEFAULT 1,
            stock_quantity INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Users table (simplified)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            first_name TEXT,
            last_name TEXT,
            phone TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Cart items table (simple, without separate cart table)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cart_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            product_id INTEGER NOT NULL,
            quantity INTEGER DEFAULT 1,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
    ''')
    
    conn.commit()
    
    # Add sample products if empty
    cursor.execute('SELECT COUNT(*) FROM products')
    if cursor.fetchone()[0] == 0:
        sample_products = [
            ('هاتف ذكي متطور', 'هاتف ذكي بمواصفات عالية وتقنيات حديثة', 2500, 'إلكترونيات', 'https://via.placeholder.com/300x300/333333/ffffff?text=هاتف', 1, 1, 10),
            ('لابتوب للألعاب', 'لابتوب قوي مخصص للألعاب والتصميم', 4500, 'إلكترونيات', 'https://via.placeholder.com/300x300/333333/ffffff?text=لابتوب', 1, 1, 5),
            ('ساعة ذكية', 'ساعة ذكية لتتبع اللياقة البدنية', 800, 'إكسسوارات', 'https://via.placeholder.com/300x300/333333/ffffff?text=ساعة', 1, 1, 15),
            ('سماعات لاسلكية', 'سماعات بلوتوث عالية الجودة', 350, 'إكسسوارات', 'https://via.placeholder.com/300x300/333333/ffffff?text=سماعات', 0, 1, 20),
            ('كاميرا رقمية', 'كاميرا احترافية للتصوير', 3200, 'إلكترونيات', 'https://via.placeholder.com/300x300/333333/ffffff?text=كاميرا', 1, 1, 8),
            ('جهاز لوحي', 'جهاز لوحي للعمل والترفيه', 1800, 'إلكترونيات', 'https://via.placeholder.com/300x300/333333/ffffff?text=تابلت', 1, 0, 0)
        ]
        
        cursor.executemany('''
            INSERT INTO products (name, description, price, category, image_url, featured, in_stock, stock_quantity)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', sample_products)
        
    conn.commit()
    conn.close()

def get_db_connection():
    """Get a database connection"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # This allows us to access columns by name
    return conn

def get_all_products():
    """Get all products"""
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products ORDER BY created_at DESC').fetchall()
    conn.close()
    return products

def get_featured_products():
    """Get featured products"""
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products WHERE featured = 1 LIMIT 6').fetchall()
    conn.close()
    return products

def get_product_by_id(product_id):
    """Get a single product by ID"""
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    conn.close()
    return product

def search_products(query, category=None):
    """Search products"""
    conn = get_db_connection()
    
    if category:
        products = conn.execute('''
            SELECT * FROM products 
            WHERE (name LIKE ? OR description LIKE ?) AND category = ?
            ORDER BY name
        ''', (f'%{query}%', f'%{query}%', category)).fetchall()
    else:
        products = conn.execute('''
            SELECT * FROM products 
            WHERE name LIKE ? OR description LIKE ?
            ORDER BY name
        ''', (f'%{query}%', f'%{query}%')).fetchall()
    
    conn.close()
    return products

def get_products_by_category(category):
    """Get products by category"""
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products WHERE category = ?', (category,)).fetchall()
    conn.close()
    return products

def get_categories():
    """Get all unique categories"""
    conn = get_db_connection()
    categories = conn.execute('SELECT DISTINCT category FROM products ORDER BY category').fetchall()
    conn.close()
    return [cat['category'] for cat in categories]

def get_related_products(product_id, category):
    """Get related products from same category"""
    conn = get_db_connection()
    products = conn.execute('''
        SELECT * FROM products 
        WHERE category = ? AND id != ? 
        LIMIT 4
    ''', (category, product_id)).fetchall()
    conn.close()
    return products

# User functions
def create_user(username, email, password_hash, first_name=None, last_name=None, phone=None):
    """Create a new user"""
    conn = get_db_connection()
    try:
        cursor = conn.execute('''
            INSERT INTO users (username, email, password_hash, first_name, last_name, phone)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (username, email, password_hash, first_name, last_name, phone))
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return user_id
    except sqlite3.IntegrityError:
        conn.close()
        return None

def get_user_by_username(username):
    """Get user by username"""
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()
    return user

def get_user_by_id(user_id):
    """Get user by ID"""
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    return user

def get_user_by_email(email):
    """Get user by email"""
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    conn.close()
    return user

# Cart functions
def add_to_cart(user_id, product_id, quantity=1):
    """Add item to cart"""
    conn = get_db_connection()
    
    # Check if item already exists
    existing = conn.execute('''
        SELECT * FROM cart_items WHERE user_id = ? AND product_id = ?
    ''', (user_id, product_id)).fetchone()
    
    if existing:
        # Update quantity
        conn.execute('''
            UPDATE cart_items SET quantity = quantity + ? WHERE user_id = ? AND product_id = ?
        ''', (quantity, user_id, product_id))
    else:
        # Add new item
        conn.execute('''
            INSERT INTO cart_items (user_id, product_id, quantity)
            VALUES (?, ?, ?)
        ''', (user_id, product_id, quantity))
    
    conn.commit()
    conn.close()

def get_cart_items(user_id):
    """Get all cart items for a user"""
    conn = get_db_connection()
    items = conn.execute('''
        SELECT ci.*, p.name, p.price, p.image_url, p.category, p.in_stock,
               (ci.quantity * p.price) as total_price
        FROM cart_items ci
        JOIN products p ON ci.product_id = p.id
        WHERE ci.user_id = ?
        ORDER BY ci.added_at DESC
    ''', (user_id,)).fetchall()
    conn.close()
    return items

def get_cart_count(user_id):
    """Get total items count in cart"""
    conn = get_db_connection()
    result = conn.execute('''
        SELECT SUM(quantity) as total FROM cart_items WHERE user_id = ?
    ''', (user_id,)).fetchone()
    conn.close()
    return result['total'] if result['total'] else 0

def get_cart_total(user_id):
    """Get total price of cart"""
    conn = get_db_connection()
    result = conn.execute('''
        SELECT SUM(ci.quantity * p.price) as total
        FROM cart_items ci
        JOIN products p ON ci.product_id = p.id
        WHERE ci.user_id = ?
    ''', (user_id,)).fetchone()
    conn.close()
    return result['total'] if result['total'] else 0

def update_cart_item(item_id, quantity, user_id):
    """Update cart item quantity"""
    conn = get_db_connection()
    if quantity <= 0:
        conn.execute('DELETE FROM cart_items WHERE id = ? AND user_id = ?', (item_id, user_id))
    else:
        conn.execute('''
            UPDATE cart_items SET quantity = ? WHERE id = ? AND user_id = ?
        ''', (quantity, item_id, user_id))
    conn.commit()
    conn.close()

def remove_cart_item(item_id, user_id):
    """Remove item from cart"""
    conn = get_db_connection()
    conn.execute('DELETE FROM cart_items WHERE id = ? AND user_id = ?', (item_id, user_id))
    conn.commit()
    conn.close()

def clear_cart(user_id):
    """Clear all items from cart"""
    conn = get_db_connection()
    conn.execute('DELETE FROM cart_items WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()