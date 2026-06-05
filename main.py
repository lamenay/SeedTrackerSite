from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Planting, Seed
from app.forms import UserSettingsForm
from app.utils import get_watering_advice
from datetime import date

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/dashboard')
@login_required
def dashboard():
    seeds_count = Seed.query.filter_by(user_id=current_user.id).count()
    plantings_list = Planting.query.filter_by(user_id=current_user.id).all()

    # Собираем информацию о поливе для каждой посадки
    watering_alerts = []
    for p in plantings_list:
        info = get_watering_advice(p, current_user.city)
        if info['advice'] in ('water_now', 'water_tomorrow', 'rain_expected'):
            watering_alerts.append({
                'planting': p,
                'info': info,
            })

    return render_template('dashboard.html',
                           seeds_count=seeds_count,
                           plantings=plantings_list,
                           watering_alerts=watering_alerts)


@main.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = UserSettingsForm()
    if form.validate_on_submit():
        current_user.city = form.city.data
        db.session.commit()
        flash('Город успешно обновлён!', 'success')
        return redirect(url_for('main.dashboard'))

    form.city.data = current_user.city
    return render_template('settings.html', form=form)
from flask import current_app

@main.route('/sw.js')
def sw():
    return current_app.send_static_file('sw.js')

@main.route('/manifest.json')
def manifest():
    return current_app.send_static_file('manifest.json')
