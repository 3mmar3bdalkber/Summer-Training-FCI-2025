import os
from flask import Flask
from flask_login import LoginManager
from models import db, User

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# Login manager setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'يرجى تسجيل الدخول للوصول لهذه الصفحة'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create tables
with app.app_context():
    db.create_all()
    
    # Add sample products if database is empty
    from models import Product
    if Product.query.count() == 0:
        sample_products = [
            Product(
                name='هاتف ذكي متطور',
                description='هاتف ذكي بمواصفات عالية وتقنيات حديثة',
                price=2500,
                category='إلكترونيات',
                image_url='https://via.placeholder.com/300x300/333333/ffffff?text=هاتف',
                featured=True,
                in_stock=True,
                stock_quantity=10
            ),
            Product(
                name='لابتوب للألعاب',
                description='لابتوب قوي مخصص للألعاب والتصميم',
                price=4500,
                category='إلكترونيات',
                image_url='https://via.placeholder.com/300x300/333333/ffffff?text=لابتوب',
                featured=True,
                in_stock=True,
                stock_quantity=5
            ),
            Product(
                name='ساعة ذكية',
                description='ساعة ذكية لتتبع اللياقة البدنية',
                price=800,
                category='إكسسوارات',
                image_url='https://via.placeholder.com/300x300/333333/ffffff?text=ساعة',
                featured=True,
                in_stock=True,
                stock_quantity=15
            ),
            Product(
                name='سماعات لاسلكية',
                description='سماعات بلوتوث عالية الجودة',
                price=350,
                category='إكسسوارات',
                image_url='https://via.placeholder.com/300x300/333333/ffffff?text=سماعات',
                featured=False,
                in_stock=True,
                stock_quantity=20
            ),
            Product(
                name='كاميرا رقمية',
                description='كاميرا احترافية للتصوير',
                price=3200,
                category='إلكترونيات',
                image_url='https://via.placeholder.com/300x300/333333/ffffff?text=كاميرا',
                featured=True,
                in_stock=True,
                stock_quantity=8
            ),
            Product(
                name='جهاز لوحي',
                description='جهاز لوحي للعمل والترفيه',
                price=1800,
                category='إلكترونيات',
                image_url='https://via.placeholder.com/300x300/333333/ffffff?text=تابلت',
                featured=True,
                in_stock=False,
                stock_quantity=0
            )
        ]
        
        for product in sample_products:
            db.session.add(product)
        db.session.commit()

# Import routes after app creation to avoid circular imports
from routes import *
