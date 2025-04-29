from flask import Flask, render_template, request, redirect, url_for, session, flash,  jsonify, request
from datetime import datetime
import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID



app = Flask(name)
app.secret_key = 'your_secret_key_here'

# Mock data for menu items
menu_items = {
    'taomlar': [
        {'id': 1, 'name': 'Osh', 'price': 25000, 'image': 'osh.jpg', 'description': 'An\'anaviy osh'},
        {'id': 2, 'name': 'Manti', 'price': 18000, 'image': 'manti.jpg', 'description': 'Qo\'y go\'shtidan manti'},
        {'id': 3, 'name': 'Lag\'mon', 'price': 22000, 'image': 'lagmon.jpg', 'description': 'Qo\'lda yorilgan lag\'mon'},
        {'id': 8, 'name': 'Somsa', 'price': 12000, 'image': 'somsa.jpg', 'description': 'Tandirda pishirilgan somsa'},
        {'id': 9, 'name': 'Chuchvara', 'price': 16000, 'image': 'chuchvara.jpg', 'description': 'Qo\'y go\'shtli chuchvara'},
        {'id': 10, 'name': 'Qozon Kabob', 'price': 28000, 'image': 'qozon_kabob.jpg', 'description': 'Qozonda pishirilgan kabob'},
        {'id': 11, 'name': 'Dimlama', 'price': 24000, 'image': 'dimlama.jpg', 'description': 'Go\'sht va sabzavotli dimlama'},
    ],
    'shirinliklar': [
        {'id': 4, 'name': 'Halva', 'price': 12000, 'image': 'halva.jpg', 'description': 'Uy halvasi'},
        {'id': 5, 'name': 'Chak-chak', 'price': 15000, 'image': 'chakchak.jpg', 'description': 'Shirin chak-chak'},
        {'id': 12, 'name': 'Qandolat', 'price': 10000, 'image': 'qandolat.jpg', 'description': 'An\'anaviy qandolat'},
        {'id': 13, 'name': 'Uzum', 'price': 8000, 'image': 'uzum.jpg', 'description': 'Tabiiy uzum'},
        {'id': 14, 'name': 'Qovun', 'price': 9000, 'image': 'qovun.jpg', 'description': 'Tarkibida shakar ko\'p'},
    ],
    'ichimliklar': [
        {'id': 6, 'name': 'Choy', 'price': 5000, 'image': 'choy.jpg', 'description': 'Yaxna choy'},
        {'id': 7, 'name': 'Qatiq', 'price': 8000, 'image': 'qatiq.jpg', 'description': 'Tabiiy qatiq'},
        {'id': 15, 'name': 'Ayron', 'price': 7000, 'image': 'ayron.jpg', 'description': 'Sovuq ayron'},
        {'id': 16, 'name': 'Fresh', 'price': 12000, 'image': 'fresh.jpg', 'description': 'Mevali fresh'},
        {'id': 17, 'name': 'Kofe', 'price': 10000, 'image': 'kofe.jpg', 'description': 'Arabcha kofe'},
        {'id': 18, 'name': 'Sok', 'price': 8000, 'image': 'sok.jpg', 'description': 'Tabiiy meva sharbati'},
    ]
}


# Mock data for tables
tables = [
    {'id': 1, 'seats': 2, 'position': (15, 20), 'shape': 'round', 'reserved': False},
    {'id': 2, 'seats': 4, 'position': (30, 25), 'shape': 'round', 'reserved': False},
    {'id': 3, 'seats': 6, 'position': (50, 20), 'shape': 'rect', 'reserved': True},
    {'id': 4, 'seats': 4, 'position': (70, 30), 'shape': 'round', 'reserved': False},
    {'id': 5, 'seats': 8, 'position': (40, 60), 'shape': 'rect', 'reserved': False},
    {'id': 6, 'seats': 2, 'position': (20, 70), 'shape': 'round', 'reserved': True},
    {'id': 7, 'seats': 4, 'position': (60, 70), 'shape': 'square', 'reserved': False},
]

# Time slots for reservation
time_slots = [
    '10:00', '11:00', '12:00', '13:00', '14:00', 
    '15:00', '16:00', '17:00', '18:00', '19:00',
    '20:00', '21:00'
]
# Filliallar ma'lumotlari
branches = [
    {
        'id': 1,
        'name': "MOSEMAOR Yunusobod",
        'address': "Yunusobod tumani, Navoiy ko'chasi 45",
        'phone': "+998901234567",
        'hours': "09:00 - 23:00",
        'location': {
            'lat': 41.3385,
            'lng': 69.3343
        }
    },
    {
        'id': 2,
        'name': "MOSEMAOR Chilonzor",
        'address': "Chilonzor tumani, Bunyodkor shoh ko'chasi 12",
        'phone': "+998901234568",
        'hours': "10:00 - 22:00",
        'location': {
            'lat': 41.2987,
            'lng': 69.2401
        }
    },
    {
        'id': 3,
        'name': "MOSEMAOR Mirzo Ulug'bek",
        'address': "Mirzo Ulug'bek tumani, Amir Temur shoh ko'chasi 78",
        'phone': "+998901234569",
        'hours': "08:00 - 24:00",
        'location': {
            'lat': 41.3153,
            'lng': 69.2817
        }
    }
]

@app.route('/api/branches', methods=['GET'])
def get_branches():
    return jsonify(branches)

@app.route('/api/nearby_branches', methods=['GET'])
def get_nearby_branches():
    lat = request.args.get('lat', type=float)
    lng = request.args.get('lng', type=float)
    
    if not lat or not lng:
        return jsonify({'error': 'Latitude and longitude required'}), 400
    
    # Har bir fillialga masofani hisoblash
    for branch in branches:
        branch['distance'] = calculate_distance(
            lat, lng,
            branch['location']['lat'], branch['location']['lng']
        )
    
    # Eng yaqin 3 ta fillialni saralash
    nearby = sorted(branches, key=lambda x: x['distance'])[:3]
    
    return jsonify(nearby)

def calculate_distance(lat1, lng1, lat2, lng2):
    # Haversine formulasi orqali masofani hisoblash
    from math import radians, sin, cos, sqrt, atan2
    
    R = 6371.0  # Earth radius in km
    
    lat1 = radians(lat1)
    lng1 = radians(lng1)
    lat2 = radians(lat2)
    lng2 = radians(lng2)
    
    dlng = lng2 - lng1
    dlat = lat2 - lat1
    
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlng / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    return R * c
@app.route('/reservation')
def reservation():
    today = datetime.now().strftime('%Y-%m-%d')
    return render_template('reservation.html', tables=tables, time_slots=time_slots, today=today)

# ... avvalgi kodlar ...

@app.route('/reset_password')
def reset_password():
    return "Parolni tiklash sahifasi hali tayyor emas."

@app.route('/make_reservation', methods=['POST'])
def make_reservation():
    if request.method == 'POST':
        reservation_data = {
            'table_id': request.form['table_id'],
            'name': request.form['name'],
            'phone': request.form['phone'],
            'date': request.form['date'],
            'time': request.form['time'],
            'guests': request.form['guests'],
            'notes': request.form.get('notes', ''),
            'branch_id': request.form.get('branch_id')
        }
        
        # Telegramga xabar yuborish
        send_telegram_notification(reservation_data)
        
        flash(f"Stol #{reservation_data['table_id']} muvaffaqiyatli band qilindi!", 'success')
        return redirect(url_for('home'))
    
    return redirect(url_for('reservation'))
def send_telegram_notification(table_id, name, phone, date, time, guests):
    # Bu funksiya Telegram bot orqali xabar yuboradi
    # Haqiqiy loyihada Telegram API bilan ishlash kerak
    print(f"Telegramga yuborildi: Stol #{table_id}, {name}, {phone}, {date} {time}, {guests} kishi")

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/menu')
def menu():
    category = request.args.get('category', 'taomlar')
    return render_template('menu.html', 
                         items=menu_items.get(category, []),
                         categories=menu_items.keys(),
                         active_category=category)
@app.route('/favorites')
def favorites():
    if 'user' not in session:
        flash('Iltimos, avval tizimga kiring', 'warning')
        return redirect(url_for('login'))
    
    favorites = session.get('favorites', [])
    fav_items = []
    for category in menu_items.values():
        for item in category:
            if item['id'] in favorites:
                fav_items.append(item)
    
    return render_template('favorites.html', items=fav_items)

@app.route('/add_to_favorites/<int:item_id>')
def add_to_favorites(item_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    
    if 'favorites' not in session:
        session['favorites'] = []
    
    if item_id not in session['favorites']:
        session['favorites'].append(item_id)
        session.modified = True
        flash('Mahsulot sevimlilarga qo\'shildi', 'success')
    
    return redirect(request.referrer)

@app.route('/cart')
def cart():
    cart_items = session.get('cart', {})
    items = []
    total = 0
    
    for category in menu_items.values():
        for item in category:
            if str(item['id']) in cart_items:
                quantity = cart_items[str(item['id'])]
                items.append({
                    'id': item['id'],
                    'name': item['name'],
                    'price': item['price'],
                    'image': item['image'],
                    'quantity': quantity,
                    'subtotal': item['price'] * quantity
                })
                total += item['price'] * quantity
    
    return render_template('cart.html', items=items, total=total)

@app.route('/add_to_cart/<int:item_id>')
def add_to_cart(item_id):
    if 'cart' not in session:
        session['cart'] = {}
    
    cart = session['cart']
    cart[str(item_id)] = cart.get(str(item_id), 0) + 1
    session.modified = True
    flash('Mahsulot savatchaga qo\'shildi', 'success')
    
    return redirect(request.referrer)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Simple authentication (in real app, use proper auth)
        if username == 'user' and password == 'password':
            session['user'] = username
            flash('Muvaffaqiyatli kirdingiz!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Noto\'g\'ri login yoki parol', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Here you would typically save to database
        session['user'] = username
        flash('Muvaffaqiyatli ro\'yxatdan o\'tdingiz!', 'success')
        return redirect(url_for('home'))
    
    return render_template('register.html')


# Savatcha bilan ishlash
@app.route('/update_cart/<int:item_id>/<int:change>', methods=['POST'])
def update_cart(item_id, change):
    if 'cart' not in session:
        session['cart'] = {}
    
    cart = session['cart']
    current_qty = cart.get(str(item_id), 0)
    new_qty = current_qty + change
    
    if new_qty <= 0:
        cart.pop(str(item_id), None)
    else:
        cart[str(item_id)] = new_qty
    
    session.modified = True
    return jsonify({'success': True})

@app.route('/remove_from_cart/<int:item_id>', methods=['POST'])
def remove_from_cart(item_id):
    if 'cart' in session:
        session['cart'].pop(str(item_id), None)
        session.modified = True
    return jsonify({'success': True})
# Buyurtma berish
@app.route('/order')
def order():
    if 'cart' not in session or not session['cart']:
        flash('Savatchangiz bo\'sh', 'warning')
        return redirect(url_for('menu'))
    
    cart_items = session.get('cart', {})
    items = []
    total = 0
    
    for category in menu_items.values():
        for item in category:
            if str(item['id']) in cart_items:
                quantity = cart_items[str(item['id'])]
                items.append({
                    'id': item['id'],
                    'name': item['name'],
                    'price': item['price'],
                    'image': item['image'],
                    'quantity': quantity,
                    'subtotal': item['price'] * quantity
                })
                total += item['price'] * quantity
    
    return render_template('order.html', items=items, total=total)

@app.route('/submit_order', methods=['POST'])
def submit_order():
    if 'cart' not in session or not session['cart']:
        flash('Savatchangiz bo\'sh', 'danger')
        return redirect(url_for('menu'))
    
    # Buyurtma ma'lumotlarini olish
    order_data = {
        'name': request.form['name'],
        'phone': request.form['phone'],
        'address': request.form['address'],
        'payment': request.form['payment'],
        'notes': request.form.get('notes', ''),
        'items': [],
        'total': 0
    }
    
    # Savatchadagi mahsulotlarni qo'shish
    for category in menu_items.values():
        for item in category:
            if str(item['id']) in session['cart']:
                quantity = session['cart'][str(item['id'])]
                order_data['items'].append({
                    'id': item['id'],
                    'name': item['name'],
                    'price': item['price'],
                    'quantity': quantity
                })
                order_data['total'] += item['price'] * quantity
    
    # Bu yerda buyurtmani ma'lumotlar bazasiga yozish kerak
    # orders_db.insert(order_data)
    
    # Telegramga xabar yuborish
    send_telegram_notification(order_data)
    
    # Savatchani tozalash
    session.pop('cart', None)
    
    flash('Buyurtmangiz qabul qilindi! Tez orada siz bilan bog\'lanamiz.', 'success')
    return redirect(url_for('home'))

import requests

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    requests.post(url, data=data)


def send_telegram_notification(reservation_data):
    """Telegramga band qilingan stol haqida xabar yuborish"""
    try:
        message = f"🚨 <b>Yangi stol band qilindi!</b>\n\n"
        message += f"👤 <b>Mijoz:</b> {reservation_data['name']}\n"
        message += f"📞 <b>Telefon:</b> {reservation_data['phone']}\n"
        message += f"🍽 <b>Stol:</b> #{reservation_data['table_id']}\n"
        message += f"📅 <b>Sana:</b> {reservation_data['date']} {reservation_data['time']}\n"
        message += f"👥 <b>Mehmonlar soni:</b> {reservation_data['guests']}\n"
        
        if reservation_data.get('branch_id'):
            branch = next(b for b in branches if b['id'] == reservation_data['branch_id'])
            message += f"🏢 <b>Fillial:</b> {branch['name']}\n"
        
        if reservation_data.get('notes'):
            message += f"📝 <b>Izoh:</b> {reservation_data['notes']}\n"
        
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            'chat_id': TELEGRAM_CHAT_ID,
            'text': message,
            'parse_mode': 'HTML'
        }
        
        response = requests.post(url, data=payload)
        return response.status_code == 200
    except Exception as e:
        print(f"Telegram xabar yuborishda xatolik: {e}")
        return False
    # Fikr-mulohazalar
@app.route('/reviews')
def reviews():
    # Haqiqiy loyihada ma'lumotlar bazasidan olish kerak
    reviews_list = [
        {
            'name': 'Ali Valiyev',
            'date': datetime(2023, 5, 15),
            'rating': 5,
            'comment': 'Ajoyib taomlar, xizmat ham zo\'r!'
        },
        {
            'name': 'Dilfuza Rahimova',
            'date': datetime(2023, 6, 2),
            'rating': 4,
            'comment': 'Yaxshi, lekin kutish vaqti uzun edi.'
        }
    ]
    return render_template('reviews.html', reviews=reviews_list)

@app.route('/add_review', methods=['POST'])
def add_review():
    if request.method == 'POST':
        rating = int(request.form['rating'])
        comment = request.form['comment']
        
        if 'user' in session:
            name = session['user']['name']
            email = session['user']['email']
        else:
            name = request.form['review_name']
            email = request.form.get('review_email', '')
        
        # Haqiqiy loyihada ma'lumotlar bazasiga yozish kerak
        # new_review = {
        #     'name': name,
        #     'email': email,
        #     'rating': rating,
        #     'comment': comment,
        #     'date': datetime.now()
        # }
        # reviews_db.insert(new_review)
        
        flash('Fikringiz uchun rahmat!', 'success')
        return redirect(url_for('reviews'))
    
    return redirect(url_for('reviews'))



@app.route('/social-login/<provider>')
def social_login(provider):
    if provider == 'google':
        # Bu yerda Google login jarayonini boshlash kodi bo'ladi
        return redirect('https://accounts.google.com/o/oauth2/auth')
    else:
        return "Provider not supported", 400


@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Siz tizimdan chiqdingiz', 'info')
    return redirect(url_for('home'))

@app.route('/admin')
def admin():
    if 'user' not in session or session['user'] != 'admin':
        flash('Admin paneliga kirish uchun ruxsat yo\'q', 'danger')
        return redirect(url_for('login'))
    
    # In real app, get reservations and orders from database
    return render_template('admin.html')

if __name__ == '__main__':
    app.run(debug=True)