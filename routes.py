from flask import render_template, request, redirect, url_for, flash
from app import app
from data import products_data, get_product_by_id, add_product, update_product, delete_product

@app.route('/')
def index():
    """Homepage with hero section and featured products"""
    featured_products = [p for p in products_data.values() if p.get('featured', False)][:6]
    return render_template('index.html', featured_products=featured_products)

@app.route('/products')
def products():
    """Product listing page"""
    category = request.args.get('category', '')
    search = request.args.get('search', '')
    
    filtered_products = products_data.values()
    
    if category:
        filtered_products = [p for p in filtered_products if p['category'] == category]
    
    if search:
        filtered_products = [p for p in filtered_products 
                           if search.lower() in p['name'].lower() or 
                           search.lower() in p['description'].lower()]
    
    categories = list(set(p['category'] for p in products_data.values()))
    
    return render_template('products.html', 
                         products=filtered_products, 
                         categories=categories,
                         current_category=category,
                         search_term=search)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    """Individual product detail page"""
    product = get_product_by_id(product_id)
    if not product:
        flash('المنتج غير موجود', 'error')
        return redirect(url_for('products'))
    
    # Get related products from same category
    related_products = [p for p in products_data.values() 
                       if p['category'] == product['category'] and p['id'] != product_id][:4]
    
    return render_template('product_detail.html', 
                         product=product, 
                         related_products=related_products)

@app.route('/about')
def about():
    """About us page"""
    return render_template('index.html', page_title='من نحن')

@app.route('/contact')
def contact():
    """Contact us page"""
    return render_template('index.html', page_title='تواصل معنا')

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors"""
    return render_template('index.html', error='الصفحة غير موجودة'), 404

@app.errorhandler(500)
def internal_server_error(e):
    """Handle 500 errors"""
    return render_template('index.html', error='خطأ في الخادم'), 500
