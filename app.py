from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, current_app
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
from config import Config
import json
from flask_migrate import Migrate 
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

# ------------------------
# Database Models
# -----------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    bookings = db.relationship('TableBooking', backref='user', lazy=True)
    orders = db.relationship('Order', backref='user', lazy=True)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    products = db.relationship('Product', backref='category', lazy=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(100))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    order_items = db.relationship('OrderItem', backref='product', lazy=True)

class RestaurantTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, unique=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    bookings = db.relationship('TableBooking', backref='table', lazy=True)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    total_amount = db.Column(db.Integer)
    status = db.Column(db.String(20), default='pending')
    items = db.relationship('OrderItem', backref='order', lazy=True)

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    price = db.Column(db.Integer)

class TableBooking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    table_id = db.Column(db.Integer, db.ForeignKey('restaurant_table.id'), nullable=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    booking_datetime = db.Column(db.DateTime, nullable=False)
    guests = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')

# ----------------------------------------
# Database Initialization
# ----------------------------------------
with app.app_context():
    db.create_all()

    # Add initial categories and products if they don't exist
    if not Category.query.first():
        initial_categories = [
            "O'zbek taomlari", 'Ichimliklar', 'Shirinliklar', 
            'Fast food (milliy)', 'Salatlar'
        ]
        for cat in initial_categories:
            db.session.add(Category(name=cat))
        
        products = [
            ('Palov', "O'zbek taomi", 45000, "O'zbek taomlari", 'plov.jpg'),
            ('Lag\'mon', "O'zbek taomi", 35000, "O'zbek taomlari", 'lagmon.jpg'),
            ('Somsa', "O'zbek taomi", 10000, "O'zbek taomlari", 'somsa.jpg'),
            ('Manti', "O'zbek taomi", 25000, "O'zbek taomlari", 'manti.jpg'),
            ('Shurva', "O'zbek taomi", 30000, "O'zbek taomlari", 'shurva.jpg'),
            ('Choy', 'Ichimlik', 5000, 'Ichimliklar', 'choy.jpg'),
            ('Qatiq', 'Ichimlik', 4000, 'Ichimliklar', 'qatiq.jpg'),
            ('Sharbat', 'Ichimlik', 8000, 'Ichimliklar', 'juice.jpg'),
            ('Suv', 'Ichimlik', 3000, 'Ichimliklar', 'water.jpg'),
            ('Kofe', 'Ichimlik', 12000, 'Ichimliklar', 'coffee.jpg'),
            ('Halva', 'Shirinlik', 15000, 'Shirinliklar', 'halva.jpg'),
            ('Pishiriq', 'Shirinlik', 20000, 'Shirinliklar', 'cake.jpg'),
            ('Qovurilgan banan', 'Shirinlik', 18000, 'Shirinliklar', 'banana.jpg'),
            ('Oshburger', 'Fast food', 25000, 'Fast food (milliy)', 'oshburger.jpg'),
            ('Shashlik roll', 'Fast food', 28000, 'Fast food (milliy)', 'shashlikroll.jpg'),
            ('Qozon kabob', 'Fast food', 32000, 'Fast food (milliy)', 'qozonkabob.jpg'),
            ('Achchiq salat', 'Salat', 12000, 'Salatlar', 'salad.jpg'),
            ('Sabzavotli salat', 'Salat', 10000, 'Salatlar', 'vegsalad.jpg'),
            ('Qatiqli salat', 'Salat', 11000, 'Salatlar', 'yogurt_salad.jpg')
        ]
        
        for name, description, price, category_name, image in products:
            category = Category.query.filter_by(name=category_name).first()
            db.session.add(Product(
                name=name,
                description=description,
                price=price,
                category_id=category.id,
                image=image
            ))
    
    # Add restaurant tables if they don't exist
    if not RestaurantTable.query.first():
        tables = [
            {"number": 1, "capacity": 2},
            {"number": 2, "capacity": 4},
            {"number": 3, "capacity": 4},
            {"number": 4, "capacity": 6},
            {"number": 5, "capacity": 8},
            {"number": 6, "capacity": 2},
            {"number": 7, "capacity": 4},
            {"number": 8, "capacity": 6},
            {"number": 9, "capacity": 10}
        ]
        
        for table in tables:
            db.session.add(RestaurantTable(
                number=table["number"],
                capacity=table["capacity"]
            ))
    
    db.session.commit()

# ------------------------
# Routes
# ------------------------





@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if 'user_id' not in session:
        flash('Iltimos, avval tizimga kiring!', 'warning')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        try:
            booking_datetime = datetime.strptime(
                f"{request.form['date']} {request.form['time']}", 
                "%Y-%m-%d %H:%M"
            )
            
            if booking_datetime < datetime.now():
                flash('Siz o\'tgan vaqt uchun stol band qila olmaysiz!', 'danger')
                return redirect(url_for('booking'))
            
            # Stol band qilishni tekshirish
            existing_booking = TableBooking.query.filter(
                TableBooking.table_id == request.form['table_id'],
                TableBooking.booking_datetime.between(
                    booking_datetime - timedelta(hours=2),
                    booking_datetime + timedelta(hours=2)
                ),
                TableBooking.status.in_(['pending', 'confirmed'])
            ).first()
            
            if existing_booking:
                flash('Ushbu vaqtda stol band! Iltimos, boshqa vaqt tanlang.', 'danger')
                return redirect(url_for('booking'))
            
            new_booking = TableBooking(
                user_id=session['user_id'],
                table_id=request.form['table_id'],
                name=request.form['name'],
                phone=request.form['phone'],
                booking_datetime=booking_datetime,
                guests=request.form['guests'],
                notes=request.form.get('notes', ''),
                status='pending'
            )
            
            db.session.add(new_booking)
            db.session.commit()
            flash('Stol muvaffaqiyatli band qilindi! Tez orada siz bilan bog\'lanamiz.', 'success')
            return redirect(url_for('index'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Xatolik yuz berdi: {str(e)}', 'danger')
    
    # GET so'rovi uchun
    tables = RestaurantTable.query.all()
    now = datetime.now()
    
    # Har bir stolning bandligini tekshirish
    for table in tables:
        table.reserved = TableBooking.query.filter(
            TableBooking.table_id == table.id,
            TableBooking.booking_datetime.between(
                now,
                now + timedelta(hours=2)
            ),
            TableBooking.status.in_(['pending', 'confirmed'])
        ).first() is not None
    
    return render_template('booking.html', tables=tables)
@app.route('/api/book_table', methods=['POST'])
def api_book_table():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Iltimos, avval tizimga kiring!'})
    
    try:
        data = request.get_json()
        booking_datetime = datetime.strptime(
            f"{data['date']} {data['time']}", 
            "%Y-%m-%d %H:%M"
        )
        
        booking = TableBooking(
            user_id=session['user_id'],
            table_id=data['table_id'],
            name=data['name'],
            phone=data['phone'],
            booking_datetime=booking_datetime,
            guests=data['guests'],
            notes=data.get('notes', ''),
            status='confirmed'
        )
        db.session.add(booking)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Stol muvaffaqiyatli band qilindi!'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400


@app.route('/admin/products')
def admin_products():
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Sizga ruxsat yo\'q!', 'danger')
        return redirect(url_for('index'))
    
    products = Product.query.all()
    categories = Category.query.all()
    return render_template('admin/products.html', 
                         products=products, 
                         categories=categories)

if __name__ == '__main__':
    app.run(debug=True)