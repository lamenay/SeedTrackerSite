from flask import Blueprint, render_template, redirect, url_for, flash, jsonify, request
from flask_login import login_required, current_user
from app import db
from app.models import Seed, Planting, CropCatalog
from app.forms import SeedForm, PlantingForm
from app.utils import get_weather_forecast, get_watering_advice
from datetime import timedelta, date

plantings = Blueprint('plantings', __name__)


# ==================== СЕМЕНА ====================
@plantings.route('/seeds')
@login_required
def seeds():
    all_seeds = Seed.query.filter_by(user_id=current_user.id).all()
    seeds_list = [s for s in all_seeds if s.remaining_seeds > 0]
    empty_seeds = [s for s in all_seeds if s.remaining_seeds == 0]
    return render_template('seeds.html', seeds=seeds_list, empty_seeds=empty_seeds, today=date.today())


@plantings.route('/add_seed', methods=['GET', 'POST'])
@login_required
def add_seed():
    form = SeedForm()

    # Populate catalog choices
    catalog_items = CropCatalog.query.order_by(CropCatalog.crop_name, CropCatalog.variety).all()
    form.catalog_id.choices = [(0, '— Выбрать из справочника (необязательно) —')] + [
        (c.id, f"{c.emoji} {c.crop_name} — {c.variety} (полив: {c.watering_interval_days}дн, созревание: {c.days_to_harvest}дн)")
        for c in catalog_items
    ]

    if form.validate_on_submit():
        packets = form.packets_count.data or 1
        seeds_per = form.seeds_per_packet.data or 1

        # Проверка на переполнение при вычислении общего количества
        try:
            total_seeds = packets * seeds_per
            if total_seeds > 2_000_000_000:
                flash('Слишком большое общее количество семян. Уменьшите количество пакетиков или семян в пакетике.', 'danger')
                return render_template('add_seed.html', form=form, catalog_items=catalog_items, today_str=date.today().isoformat())
        except (OverflowError, ValueError):
            flash('Слишком большое значение. Пожалуйста, введите разумное количество.', 'danger')
            return render_template('add_seed.html', form=form, catalog_items=catalog_items, today_str=date.today().isoformat())

        seed = Seed(
            user_id=current_user.id,
            crop_name=form.crop_name.data,
            variety=form.variety.data,
            manufacturer=form.manufacturer.data,
            purchase_date=form.purchase_date.data,
            expiry_date=form.expiry_date.data,
            packets_count=packets,
            seeds_per_packet=seeds_per,
            remaining_seeds=total_seeds,
            catalog_id=form.catalog_id.data if form.catalog_id.data else None,
            notes=form.notes.data
        )

        try:
            db.session.add(seed)
            db.session.commit()
        except (OverflowError, Exception) as e:
            db.session.rollback()
            if 'too large' in str(e).lower() or isinstance(e, OverflowError):
                flash('Слишком большое значение для сохранения в базу данных. Уменьшите количество.', 'danger')
            else:
                flash(f'Ошибка при сохранении: {e}', 'danger')
            return render_template('add_seed.html', form=form, catalog_items=catalog_items, today_str=date.today().isoformat())

        flash('Семена успешно добавлены!', 'success')
        return redirect(url_for('plantings.seeds'))
    return render_template('add_seed.html', form=form, catalog_items=catalog_items, today_str=date.today().isoformat())


@plantings.route('/api/catalog/<int:catalog_id>')
@login_required
def get_catalog_item(catalog_id):
    """API endpoint для получения данных из справочника."""
    item = CropCatalog.query.get_or_404(catalog_id)
    return jsonify({
        'crop_name': item.crop_name,
        'variety': item.variety,
        'watering_interval_days': item.watering_interval_days,
        'days_to_harvest': item.days_to_harvest,
        'description': item.description,
        'emoji': item.emoji,
    })


# ==================== ПОСАДКИ ====================
@plantings.route('/add_planting', methods=['GET', 'POST'])
@login_required
def add_planting():
    form = PlantingForm()
    weather = get_weather_forecast(current_user.city)
    user_seeds = Seed.query.filter_by(user_id=current_user.id).filter(Seed.remaining_seeds > 0).all()
    form.seed_id.choices = [(s.id, f"{s.crop_name}{' — ' + s.variety if s.variety else ''} ({s.remaining_seeds} шт.)") for s in user_seeds]

    if form.validate_on_submit():
        seed = Seed.query.get_or_404(form.seed_id.data)

        # Проверка на просроченные семена
        if seed.expiry_date and seed.expiry_date <= date.today():
            flash(f'Нельзя посадить просроченные семена! Срок годности «{seed.crop_name}» истёк {seed.expiry_date.strftime("%d.%m.%Y")}.', 'danger')
            return redirect(url_for('plantings.add_planting'))

        if seed.remaining_seeds < form.quantity_sown.data:
            flash(f'Недостаточно семян! Осталось: {seed.remaining_seeds}', 'danger')
            return redirect(url_for('plantings.add_planting'))

        expected_date = form.sowing_date.data + timedelta(days=(form.days_to_harvest.data or 60))

        planting = Planting(
            user_id=current_user.id,
            seed_id=seed.id,
            sowing_date=form.sowing_date.data,
            quantity_sown=form.quantity_sown.data,
            location=form.location.data,
            watering_interval=form.watering_interval.data,
            days_to_harvest=form.days_to_harvest.data,
            expected_harvest_date=expected_date,
            last_watered=form.sowing_date.data,
            notes=form.notes.data
        )

        seed.remaining_seeds -= form.quantity_sown.data

        try:
            db.session.add(planting)
            db.session.commit()
        except (OverflowError, Exception) as e:
            db.session.rollback()
            if 'too large' in str(e).lower() or isinstance(e, OverflowError):
                flash('Слишком большое значение. Пожалуйста, введите разумное количество.', 'danger')
            else:
                flash(f'Ошибка при сохранении: {e}', 'danger')
            return redirect(url_for('plantings.add_planting'))

        flash(f'Посадка "{seed.crop_name}" добавлена! Осталось: {seed.remaining_seeds} семян', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('add_planting.html', form=form, weather=weather, seeds=user_seeds)


# Детальная страница посадки
@plantings.route('/planting/<int:planting_id>')
@login_required
def planting_detail(planting_id):
    planting = Planting.query.get_or_404(planting_id)
    if planting.user_id != current_user.id:
        flash('Доступ запрещён', 'danger')
        return redirect(url_for('main.dashboard'))

    today = date.today()
    days_left = (planting.expected_harvest_date - today).days if planting.expected_harvest_date else None

    # Умный совет по поливу
    watering_info = get_watering_advice(planting, current_user.city)

    return render_template('planting_detail.html',
                           planting=planting,
                           days_left=days_left,
                           watering_info=watering_info)


# Кнопка "Я полил"
@plantings.route('/planting/<int:planting_id>/water', methods=['POST'])
@login_required
def mark_watered(planting_id):
    planting = Planting.query.get_or_404(planting_id)
    if planting.user_id != current_user.id:
        flash('Доступ запрещён', 'danger')
        return redirect(url_for('main.dashboard'))

    planting.last_watered = date.today()
    planting.rain_skipped = False
    db.session.commit()
    flash('Полив отмечен! 💧', 'success')
    return redirect(url_for('plantings.planting_detail', planting_id=planting_id))


# Кнопка "Дождь полил за меня"
@plantings.route('/planting/<int:planting_id>/rain_skip', methods=['POST'])
@login_required
def rain_skip(planting_id):
    planting = Planting.query.get_or_404(planting_id)
    if planting.user_id != current_user.id:
        flash('Доступ запрещён', 'danger')
        return redirect(url_for('main.dashboard'))

    planting.last_watered = date.today()
    planting.rain_skipped = True
    db.session.commit()
    flash('Дождь засчитан как полив! 🌧', 'info')
    return redirect(url_for('plantings.planting_detail', planting_id=planting_id))


# Удаление посадки
@plantings.route('/planting/<int:planting_id>/delete')
@login_required
def delete_planting(planting_id):
    planting = Planting.query.get_or_404(planting_id)
    if planting.user_id == current_user.id:
        db.session.delete(planting)
        db.session.commit()
        flash('Посадка удалена', 'info')
    return redirect(url_for('main.dashboard'))


# Удаление семян
@plantings.route('/seed/<int:seed_id>/delete')
@login_required
def delete_seed(seed_id):
    seed = Seed.query.get_or_404(seed_id)
    if seed.user_id != current_user.id:
        flash('Доступ запрещён', 'danger')
        return redirect(url_for('plantings.seeds'))
    Planting.query.filter_by(seed_id=seed.id).delete()
    db.session.delete(seed)
    db.session.commit()
    flash('Запись о семенах удалена', 'info')
    return redirect(url_for('plantings.seeds'))