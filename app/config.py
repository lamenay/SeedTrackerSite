import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'super-secret-key-seedtracker-2026')

    # База данных
    _db_url = os.getenv('DATABASE_URL', '')
    if _db_url.startswith('postgres://'):
        _db_url = _db_url.replace('postgres://', 'postgresql://', 1)

    # Если DATABASE_URL не задан — используем /tmp (единственное место где SQLite работает на Render)
    SQLALCHEMY_DATABASE_URI = _db_url if _db_url else 'sqlite:////tmp/seedtracker.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Yandex OAuth
    YANDEX_CLIENT_ID = os.getenv('YANDEX_CLIENT_ID', '')
    YANDEX_CLIENT_SECRET = os.getenv('YANDEX_CLIENT_SECRET', '')
    YANDEX_REDIRECT_URI = os.getenv('YANDEX_REDIRECT_URI', 'http://localhost:5000/auth/yandex/callback')
