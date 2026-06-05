from app import db
from flask_login import UserMixin
from datetime import date, timedelta


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=True)  # nullable for Yandex-only users
    city = db.Column(db.String(100), default='Уфа')
    yandex_id = db.Column(db.String(100), unique=True, nullable=True)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)


class CropCatalog(db.Model):
    """Справочник культур и сортов с информацией о поливе и созревании."""
    id = db.Column(db.Integer, primary_key=True)
    crop_name = db.Column(db.String(100), nullable=False)
    variety = db.Column(db.String(150), nullable=False)
    watering_interval_days = db.Column(db.Integer, nullable=False, default=7)
    days_to_harvest = db.Column(db.Integer, nullable=False, default=60)
    description = db.Column(db.Text)
    emoji = db.Column(db.String(10), default='🌱')


class Seed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    crop_name = db.Column(db.String(100), nullable=False)
    variety = db.Column(db.String(150))
    manufacturer = db.Column(db.String(100))
    purchase_date = db.Column(db.Date)
    expiry_date = db.Column(db.Date)

    packets_count = db.Column(db.Integer, default=1)
    seeds_per_packet = db.Column(db.Integer, default=0)
    remaining_seeds = db.Column(db.Integer, default=0)

    # Link to catalog for auto-fill
    catalog_id = db.Column(db.Integer, db.ForeignKey('crop_catalog.id'), nullable=True)
    catalog_entry = db.relationship('CropCatalog', backref='seeds')

    notes = db.Column(db.Text)


class Planting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    seed_id = db.Column(db.Integer, db.ForeignKey('seed.id'), nullable=False)

    sowing_date = db.Column(db.Date, nullable=False)
    quantity_sown = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(100))

    watering_interval = db.Column(db.Integer)
    days_to_harvest = db.Column(db.Integer)
    expected_harvest_date = db.Column(db.Date)
    yield_rate = db.Column(db.Float)
    notes = db.Column(db.Text)

    # Watering tracking
    last_watered = db.Column(db.Date, nullable=True)
    rain_skipped = db.Column(db.Boolean, default=False)

    seed = db.relationship('Seed', backref='plantings')

    @property
    def next_watering_date(self):
        if not self.watering_interval:
            return None
        base = self.last_watered or self.sowing_date
        return base + timedelta(days=self.watering_interval)

    @property
    def days_until_watering(self):
        nw = self.next_watering_date
        if nw is None:
            return None
        return (nw - date.today()).days


class SeasonalEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.Integer, nullable=False)
    plant_name = db.Column(db.String(100), nullable=False)
    event_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    emoji = db.Column(db.String(10), default='🌱')
