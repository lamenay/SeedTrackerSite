from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from app.config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    Migrate(app, db)

    from app.routes.auth import auth
    from app.routes.admin import admin_bp
    from app.routes.main import main
    from app.routes.plantings import plantings
    from app.routes.calendar import calendar_bp

    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(admin_bp)
    app.register_blueprint(main)
    app.register_blueprint(plantings, url_prefix='/plantings')
    app.register_blueprint(calendar_bp, url_prefix='/calendar')

    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()
        # Создаём первого администратора если его нет
        from app.models import User
        from werkzeug.security import generate_password_hash
        if not User.query.filter_by(email='admin@seedtracker.local').first():
            admin = User(
                username='admin',
                email='admin@seedtracker.local',
                password_hash=generate_password_hash('admin123'),
                city='Москва',
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
            print('✅ Администратор создан: admin@seedtracker.local / admin123')
        seed_calendar_data()
        seed_crop_catalog()

    return app


def seed_calendar_data():
    from app.models import SeasonalEvent
    if SeasonalEvent.query.first():
        return
    events = [
        (3, "Крокус", "цветение", "Первые весенние цветы", "🌸"),
        (4, "Тюльпан", "цветение", "Яркие весенние тюльпаны", "🌷"),
        (4, "Нарцисс", "цветение", "Жёлтые весенние нарциссы", "🌼"),
        (5, "Сирень", "цветение", "Красивейший майский кустарник", "🌸"),
        (5, "Ландыш", "цветение", "Лесной и садовый ландыш", "🪻"),
        (5, "Черёмуха", "цветение", "Душистая черёмуха", "🌳"),
        (6, "Клубника", "созревание", "Первый летний урожай", "🍓"),
        (6, "Пион", "цветение", "Роскошные пионы", "🌺"),
        (6, "Роза", "цветение", "Садовые розы", "🌹"),
        (7, "Томат", "созревание", "Урожай томатов", "🍅"),
        (7, "Огурец", "созревание", "Свежие огурцы", "🥒"),
        (7, "Малина", "созревание", "Ароматная малина", "🫐"),
        (8, "Подсолнух", "цветение", "Яркие подсолнухи", "🌻"),
        (8, "Кабачок", "созревание", "Кабачки и цуккини", "🟢"),
        (9, "Яблоко", "созревание", "Осенние яблоки", "🍎"),
        (9, "Тыква", "созревание", "Урожай тыкв", "🎃"),
        (10, "Хризантема", "цветение", "Осенние хризантемы", "🌼"),
    ]
    for month, name, etype, desc, emoji in events:
        db.session.add(SeasonalEvent(month=month, plant_name=name, event_type=etype, description=desc, emoji=emoji))
    db.session.commit()


def seed_crop_catalog():
    from app.models import CropCatalog
    from app.crop_data import CROP_CATALOG
    if CropCatalog.query.first():
        return
    for item in CROP_CATALOG:
        db.session.add(CropCatalog(**item))
    db.session.commit()
