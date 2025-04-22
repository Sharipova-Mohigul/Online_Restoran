import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///mosemaor.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'static/images/products'
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}
    
    # To'lov tizimi sozlamalari
    PAYME_MERCHANT_ID = os.getenv('PAYME_MERCHANT_ID', 'your_merchant_id')
    PAYME_MERCHANT_KEY = os.getenv('PAYME_MERCHANT_KEY', 'your_merchant_key')
    TEST_MODE = os.getenv('TEST_MODE', 'True') == 'True'
    
    # Google Maps API
    GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY', 'your_api_key')
    
    # Telegram bot
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'your_bot_token')
    TELEGRAM_ADMIN_ID = os.getenv('TELEGRAM_ADMIN_ID', 'your_admin_id')