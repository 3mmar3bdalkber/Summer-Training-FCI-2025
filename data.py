"""In-memory data storage for products"""

# Sample product data
products_data = {
    1: {
        'id': 1,
        'name': 'هاتف ذكي متطور',
        'description': 'هاتف ذكي بمواصفات عالية وتقنيات حديثة',
        'price': 2500,
        'category': 'إلكترونيات',
        'image': 'https://via.placeholder.com/300x300/333333/ffffff?text=هاتف',
        'featured': True,
        'in_stock': True
    },
    2: {
        'id': 2,
        'name': 'لابتوب للألعاب',
        'description': 'لابتوب قوي مخصص للألعاب والتصميم',
        'price': 4500,
        'category': 'إلكترونيات',
        'image': 'https://via.placeholder.com/300x300/333333/ffffff?text=لابتوب',
        'featured': True,
        'in_stock': True
    },
    3: {
        'id': 3,
        'name': 'ساعة ذكية',
        'description': 'ساعة ذكية لتتبع اللياقة البدنية',
        'price': 800,
        'category': 'إكسسوارات',
        'image': 'https://via.placeholder.com/300x300/333333/ffffff?text=ساعة',
        'featured': True,
        'in_stock': True
    },
    4: {
        'id': 4,
        'name': 'سماعات لاسلكية',
        'description': 'سماعات بلوتوث عالية الجودة',
        'price': 350,
        'category': 'إكسسوارات',
        'image': 'https://via.placeholder.com/300x300/333333/ffffff?text=سماعات',
        'featured': False,
        'in_stock': True
    },
    5: {
        'id': 5,
        'name': 'كاميرا رقمية',
        'description': 'كاميرا احترافية للتصوير',
        'price': 3200,
        'category': 'إلكترونيات',
        'image': 'https://via.placeholder.com/300x300/333333/ffffff?text=كاميرا',
        'featured': True,
        'in_stock': True
    },
    6: {
        'id': 6,
        'name': 'جهاز لوحي',
        'description': 'جهاز لوحي للعمل والترفيه',
        'price': 1800,
        'category': 'إلكترونيات',
        'image': 'https://via.placeholder.com/300x300/333333/ffffff?text=تابلت',
        'featured': True,
        'in_stock': False
    }
}

def get_product_by_id(product_id):
    """Get product by ID"""
    return products_data.get(product_id)

def add_product(product_data):
    """Add new product"""
    new_id = max(products_data.keys()) + 1 if products_data else 1
    product_data['id'] = new_id
    products_data[new_id] = product_data
    return new_id

def update_product(product_id, product_data):
    """Update existing product"""
    if product_id in products_data:
        products_data[product_id].update(product_data)
        return True
    return False

def delete_product(product_id):
    """Delete product"""
    if product_id in products_data:
        del products_data[product_id]
        return True
    return False

def get_categories():
    """Get all unique categories"""
    return list(set(p['category'] for p in products_data.values()))
