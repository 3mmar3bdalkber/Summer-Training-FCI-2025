from flask import render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app import app
from models import db, Product, User, Order, OrderItem, Cart, CartItem

@app.route('/')
def index():
    """Homepage with hero section and featured products"""
    featured_products = Product.query.filter_by(featured=True).limit(6).all()
    return render_template('index.html', featured_products=featured_products)

@app.route('/products')
def products():
    """Product listing page"""
    category = request.args.get('category', '')
    search = request.args.get('search', '')
    
    # Start with all products
    query = Product.query
    
    # Filter by category if specified
    if category:
        query = query.filter(Product.category == category)
    
    # Filter by search term if specified
    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            db.or_(
                Product.name.ilike(search_filter),
                Product.description.ilike(search_filter)
            )
        )
    
    filtered_products = query.all()
    categories = db.session.query(Product.category).distinct().all()
    categories = [cat[0] for cat in categories]
    
    return render_template('products.html', 
                         products=filtered_products, 
                         categories=categories,
                         current_category=category,
                         search_term=search)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    """Individual product detail page"""
    product = Product.query.get_or_404(product_id)
    
    # Get related products from same category
    related_products = Product.query.filter(
        Product.category == product.category,
        Product.id != product_id
    ).limit(4).all()
    
    return render_template('product_detail.html', 
                         product=product, 
                         related_products=related_products)

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
    
    # Search in products using database
    search_filter = f"%{query}%"
    results_query = Product.query.filter(
        db.or_(
            Product.name.ilike(search_filter),
            Product.description.ilike(search_filter)
        )
    )
    
    if category:
        results_query = results_query.filter(Product.category == category)
    
    results = results_query.all()
    categories = db.session.query(Product.category).distinct().all()
    categories = [cat[0] for cat in categories]
    
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
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            flash(f'مرحباً بك {user.first_name or user.username}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
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
        if User.query.filter_by(username=username).first():
            flash('اسم المستخدم موجود بالفعل', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('البريد الإلكتروني مستخدم بالفعل', 'error')
            return render_template('register.html')
        
        # Create new user
        user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone=phone
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('تم إنشاء الحساب بنجاح! يمكنك الآن تسجيل الدخول', 'success')
        return redirect(url_for('login'))
    
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
    """User profile page"""
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('profile.html', orders=orders)

@app.route('/cart')
def cart():
    """Shopping cart page"""
    cart = None
    if current_user.is_authenticated:
        cart = Cart.query.filter_by(user_id=current_user.id).first()
    return render_template('cart.html', cart=cart)

@app.route('/cart/add', methods=['POST'])
@login_required
def add_to_cart():
    """Add product to cart"""
    try:
        data = request.get_json()
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)
        
        product = Product.query.get_or_404(product_id)
        
        if not product.in_stock:
            return jsonify({'success': False, 'message': 'المنتج غير متوفر'})
        
        # Get or create cart
        cart = Cart.query.filter_by(user_id=current_user.id).first()
        if not cart:
            cart = Cart(user_id=current_user.id)
            db.session.add(cart)
            db.session.flush()  # To get cart.id
        
        # Check if item already in cart
        cart_item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
        
        if cart_item:
            cart_item.quantity += quantity
        else:
            cart_item = CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity)
            db.session.add(cart_item)
        
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': 'تم إضافة المنتج للسلة',
            'cart_count': cart.total_items
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'حدث خطأ في إضافة المنتج'})

@app.route('/cart/update', methods=['POST'])
@login_required
def update_cart():
    """Update cart item quantity"""
    try:
        data = request.get_json()
        item_id = data.get('item_id')
        quantity = data.get('quantity')
        
        cart_item = CartItem.query.get_or_404(item_id)
        
        # Verify the item belongs to current user's cart
        if cart_item.cart.user_id != current_user.id:
            return jsonify({'success': False, 'message': 'غير مسموح'})
        
        if quantity <= 0:
            db.session.delete(cart_item)
        else:
            cart_item.quantity = quantity
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'تم تحديث الكمية'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'حدث خطأ في التحديث'})

@app.route('/cart/remove', methods=['POST'])
@login_required
def remove_from_cart():
    """Remove item from cart"""
    try:
        data = request.get_json()
        item_id = data.get('item_id')
        
        cart_item = CartItem.query.get_or_404(item_id)
        
        # Verify the item belongs to current user's cart
        if cart_item.cart.user_id != current_user.id:
            return jsonify({'success': False, 'message': 'غير مسموح'})
        
        db.session.delete(cart_item)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'تم حذف المنتج'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'حدث خطأ في الحذف'})

@app.route('/cart/clear', methods=['POST'])
@login_required
def clear_cart():
    """Clear all items from cart"""
    try:
        cart = Cart.query.filter_by(user_id=current_user.id).first()
        if cart:
            CartItem.query.filter_by(cart_id=cart.id).delete()
            db.session.commit()
        
        return jsonify({'success': True, 'message': 'تم إفراغ السلة'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'حدث خطأ في إفراغ السلة'})

@app.route('/cart/count')
def cart_count():
    """Get cart items count"""
    count = 0
    if current_user.is_authenticated:
        cart = Cart.query.filter_by(user_id=current_user.id).first()
        if cart:
            count = cart.total_items
    return jsonify({'count': count})

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors"""
    return render_template('index.html', error='الصفحة غير موجودة'), 404

@app.errorhandler(500)
def internal_server_error(e):
    """Handle 500 errors"""
    return render_template('index.html', error='خطأ في الخادم'), 500
