import sqlite3
from flask import render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from app import app, User
from database import (
    get_all_products, get_featured_products, get_product_by_id, search_products,
    get_products_by_category, get_categories, get_related_products,
    create_user, get_user_by_username, get_user_by_email,
    add_to_cart, get_cart_items, get_cart_count, get_cart_total,
    update_cart_item, remove_cart_item, clear_cart,add_to_wishlist,create_order,
    get_wishlist_for_user, remove_from_wishlist, is_in_wishlist, cancel_order_by_id,
    get_orders_for_user,
    DATABASE_PATH
)

@app.route('/')
def index():
    """Homepage with hero section and featured products"""
    featured_products = get_featured_products()
    return render_template('index.html', featured_products=featured_products)

@app.route('/products')
def products():
    """Product listing page"""
    category = request.args.get('category', '')
    search = request.args.get('search', '')
    
    # Get products based on filters
    if search and category:
        filtered_products = search_products(search, category)
    elif search:
        filtered_products = search_products(search)
    elif category:
        filtered_products = get_products_by_category(category)
    else:
        filtered_products = get_all_products()
    
    categories = get_categories()
    
    return render_template('products.html', 
                         products=filtered_products, 
                         categories=categories,
                         current_category=category,
                         search_term=search)


@app.route('/about')
def about():
    """About us page"""
    return render_template('about.html')

@app.route('/contact')
def contact():
    """Contact us page"""
    return render_template('contact.html')

@app.route('/search')
def search():
    """Enhanced search page"""
    query = request.args.get('q', '')
    category = request.args.get('category', '')
    
    if not query:
        return redirect(url_for('products'))
    
    # Search in products
    if category:
        results = search_products(query, category)
    else:
        results = search_products(query)
    
    categories = get_categories()
    
    return render_template('search_results.html', 
                         results=results, 
                         query=query,
                         categories=categories,
                         selected_category=category)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login page"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remember = 'remember' in request.form
        
        user_data = get_user_by_username(username)
        print(user_data)

        
        if user_data:
            user = User(user_data)
            if user.check_password(password):
                login_user(user, remember=remember)
                next_page = request.args.get('next')
                flash(f'مرحباً بك {user.first_name or user.username}!', 'success')
                return redirect(next_page) if next_page else redirect(url_for('index'))
        
        flash('اسم المستخدم أو كلمة المرور غير صحيحة', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        first_name = request.form.get('first_name', '')
        last_name = request.form.get('last_name', '')
        phone = request.form.get('phone', '')
        
        # Validation
        if password != confirm_password:
            flash('كلمات المرور غير متطابقة', 'error')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('كلمة المرور يجب أن تكون 6 أحرف على الأقل', 'error')
            return render_template('register.html')
        
        # Check if user exists
        if get_user_by_username(username):
            flash('اسم المستخدم موجود بالفعل', 'error')
            return render_template('register.html')
        
        if get_user_by_email(email):
            flash('البريد الإلكتروني مستخدم بالفعل', 'error')
            return render_template('register.html')
        
        # Create new user
        password_hash = generate_password_hash(password)
        user_id = create_user(username, email, password_hash, first_name, last_name, phone)
        
        if user_id:
            flash('تم إنشاء الحساب بنجاح! يمكنك الآن تسجيل الدخول', 'success')
            return redirect(url_for('login'))
        else:
            flash('حدث خطأ في إنشاء الحساب', 'error')
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('تم تسجيل خروجك بنجاح', 'info')
    return redirect(url_for('index'))

@app.route('/profile')
@login_required
def profile():
    orders = get_orders_for_user(current_user.id)
    return render_template('profile.html', orders=orders)

# إلغاء طلب
@app.route('/orders/cancel', methods=['POST'])
@login_required
def cancel_order():
    data = request.get_json()
    order_id = data.get('order_id')
    if not order_id:
        return jsonify({'success': False, 'message': 'رقم الطلب غير موجود'})

    success = cancel_order_by_id(current_user.id, order_id)
    if success:
        return jsonify({'success': True, 'message': 'تم إلغاء الطلب بنجاح'})
    else:
        return jsonify({'success': False, 'message': 'لا يمكن إلغاء الطلب'})

@app.route('/cart')
def cart():
    """Shopping cart page"""
    cart_items = []
    cart_total = 0
    cart_count = 0
    
    if current_user.is_authenticated:
        cart_items = get_cart_items(int(current_user.id))
        cart_total = get_cart_total(int(current_user.id))
        cart_count = get_cart_count(int(current_user.id))
    
    cart_data = {
        'items': cart_items,
        'total_price': cart_total,
        'total_items': cart_count
    }
    
    return render_template('cart.html', cart=cart_data)

@app.route('/cart/add', methods=['POST'])
@login_required
def add_to_cart_route():
    """Add product to cart"""
    try:
        data = request.get_json()
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)
        
        product = get_product_by_id(product_id)
        if not product:
            return jsonify({'success': False, 'message': 'المنتج غير موجود'})
        
        if not product['in_stock']:
            return jsonify({'success': False, 'message': 'المنتج غير متوفر'})
        
        add_to_cart(int(current_user.id), product_id, quantity)
        cart_count = get_cart_count(int(current_user.id))
        
        return jsonify({
            'success': True, 
            'message': 'تم إضافة المنتج للسلة',
            'cart_count': cart_count
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': 'حدث خطأ في إضافة المنتج'})

@app.route('/cart/update', methods=['POST'])
@login_required
def update_cart_route():
    """Update cart item quantity"""
    try:
        data = request.get_json()
        item_id = data.get('item_id')
        quantity = data.get('quantity')
        
        update_cart_item(item_id, quantity, int(current_user.id))
        
        return jsonify({'success': True, 'message': 'تم تحديث الكمية'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': 'حدث خطأ في التحديث'})

@app.route('/cart/remove', methods=['POST'])
@login_required
def remove_from_cart_route():
    """Remove item from cart"""
    try:
        data = request.get_json()
        item_id = data.get('item_id')
        
        remove_cart_item(item_id, int(current_user.id))
        
        return jsonify({'success': True, 'message': 'تم حذف المنتج'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': 'حدث خطأ في الحذف'})

@app.route('/cart/clear', methods=['POST'])
@login_required
def clear_cart_route():
    """Clear all items from cart"""
    try:
        clear_cart(int(current_user.id))
        
        return jsonify({'success': True, 'message': 'تم إفراغ السلة'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': 'حدث خطأ في إفراغ السلة'})

@app.route('/cart/count')
def cart_count_route():
    """Get cart items count"""
    count = 0
    if current_user.is_authenticated:
        count = get_cart_count(int(current_user.id))
    return jsonify({'count': count})

@app.route('/wishlist/page')
@login_required
def wishlist_page():
    user_id = current_user.id
    wishlist_ids = get_wishlist_for_user(user_id)
    
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if wishlist_ids:
        placeholders = ','.join(['?']*len(wishlist_ids))
        cursor.execute(f"SELECT * FROM products WHERE id IN ({placeholders})", wishlist_ids)
        products = cursor.fetchall()
    else:
        products = []

    conn.close()
    return render_template('wishlist_page.html', products=products)


@app.route('/wishlist/toggle', methods=['POST'])
@login_required
def toggle_wishlist():
    data = request.get_json()
    product_id = data.get('product_id')
    user_id = current_user.id

    if is_in_wishlist(user_id, product_id):
        remove_from_wishlist(user_id, product_id)
        return jsonify({'success': True, 'message': 'تم حذف المنتج من المفضلة'})
    else:
        add_to_wishlist(user_id, product_id)
        return jsonify({'success': True, 'message': 'تم إضافة المنتج للمفضلة'})

@app.route('/wishlist')
@login_required
def get_wishlist():

    user_id = current_user.id
    
    wishlist = get_wishlist_for_user(user_id)  # ترجع قائمة product_id
    return jsonify({"success": True, "wishlist": wishlist})
@app.route('/checkout', methods=['POST'])
@login_required
def checkout():
    order_id = create_order(current_user.id)
    if order_id:
        return jsonify({'success': True, 'message': f'تم إنشاء الطلب بنجاح!'})
    return jsonify({'success': False, 'message': 'السلة فارغة'})

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors"""
    return render_template('index.html', error='الصفحة غير موجودة'), 404

@app.errorhandler(500)
def internal_server_error(e):
    """Handle 500 errors"""
    return render_template('index.html', error='خطأ في الخادم'), 500
