import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'super-secret-key-seedtracker-2026')
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # Use DATABASE_URL from environment (Render provides PostgreSQL URL)
    # Fallback to SQLite for local development
    DATABASE_URL = os.getenv('DATABASE_URL', '')
    # Render uses "postgres://" but SQLAlchemy needs "postgresql://"
    if DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

    SQLALCHEMY_DATABASE_URI = DATABASE_URL or f'sqlite:///{os.path.join(BASE_DIR, "..", "instance", "seedtracker.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Yandex OAuth
    YANDEX_CLIENT_ID = os.getenv('YANDEX_CLIENT_ID', '')
    YANDEX_CLIENT_SECRET = os.getenv('YANDEX_CLIENT_SECRET', '')
    YANDEX_REDIRECT_URI = os.getenv('YANDEX_REDIRECT_URI', 'http://localhost:5000/auth/yandex/callback')
