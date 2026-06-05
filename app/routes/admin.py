from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from functools import wraps
from app import db
from app.models import User, Seed, Planting, CropCatalog, SeasonalEvent

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Доступ запрещён. Требуются права администратора.', 'danger')
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated


@admin_bp.route('/')
@login_required
@admin_required
def index():
    users_count = User.query.count()
    seeds_count = Seed.query.count()
    plantings_count = Planting.query.count()
    catalog_count = CropCatalog.query.count()
    recent_users = User.query.order_by(User.id.desc()).limit(5).all()
    return render_template('admin/index.html',
                           users_count=users_count,
                           seeds_count=seeds_count,
                           plantings_count=plantings_count,
                           catalog_count=catalog_count,
                           recent_users=recent_users)


@admin_bp.route('/users')
@login_required
@admin_required
def users():
    all_users = User.query.order_by(User.id).all()
    return render_template('admin/users.html', users=all_users)


@admin_bp.route('/users/<int:user_id>/toggle_admin', methods=['POST'])
@login_required
@admin_required
def toggle_admin(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('Нельзя изменить свои собственные права.', 'warning')
        return redirect(url_for('admin.users'))
    if user.is_admin:
        flash('Нельзя снять права администратора у другого админа.', 'warning')
        return redirect(url_for('admin.users'))
    user.is_admin = True
    db.session.commit()
    flash(f'Пользователь {user.username} назначен администратором.', 'success')
    return redirect(url_for('admin.users'))


@admin_bp.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('Нельзя удалить самого себя.', 'warning')
        return redirect(url_for('admin.users'))
    if user.is_admin:
        flash('Нельзя удалить другого администратора.', 'warning')
        return redirect(url_for('admin.users'))
    # Удаляем посадки и семена пользователя
    Planting.query.filter_by(user_id=user.id).delete()
    Seed.query.filter_by(user_id=user.id).delete()
    db.session.delete(user)
    db.session.commit()
    flash(f'Пользователь {user.username} удалён.', 'success')
    return redirect(url_for('admin.users'))


@admin_bp.route('/catalog')
@login_required
@admin_required
def catalog():
    entries = CropCatalog.query.order_by(CropCatalog.crop_name).all()
    return render_template('admin/catalog.html', entries=entries)


@admin_bp.route('/catalog/add', methods=['GET', 'POST'])
@login_required
@admin_required
def catalog_add():
    if request.method == 'POST':
        try:
            watering = int(request.form['watering_interval_days'])
            harvest = int(request.form['days_to_harvest'])
        except (ValueError, OverflowError):
            flash('Введите корректные числовые значения.', 'danger')
            return render_template('admin/catalog_form.html', entry=None)

        if watering < 1 or harvest < 1:
            flash('Интервал полива и дней до урожая должны быть положительными числами (минимум 1).', 'danger')
            return render_template('admin/catalog_form.html', entry=None)

        if watering > 2_000_000_000 or harvest > 2_000_000_000:
            flash('Слишком большое значение. Введите разумное число.', 'danger')
            return render_template('admin/catalog_form.html', entry=None)

        entry = CropCatalog(
            crop_name=request.form['crop_name'],
            variety=request.form['variety'],
            watering_interval_days=watering,
            days_to_harvest=harvest,
            description=request.form.get('description', ''),
            emoji=request.form.get('emoji', '🌱'),
        )
        db.session.add(entry)
        db.session.commit()
        flash(f'Культура «{entry.crop_name} — {entry.variety}» добавлена.', 'success')
        return redirect(url_for('admin.catalog'))
    return render_template('admin/catalog_form.html', entry=None)


@admin_bp.route('/catalog/<int:entry_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def catalog_edit(entry_id):
    entry = CropCatalog.query.get_or_404(entry_id)
    if request.method == 'POST':
        try:
            watering = int(request.form['watering_interval_days'])
            harvest = int(request.form['days_to_harvest'])
        except (ValueError, OverflowError):
            flash('Введите корректные числовые значения.', 'danger')
            return render_template('admin/catalog_form.html', entry=entry)

        if watering < 1 or harvest < 1:
            flash('Интервал полива и дней до урожая должны быть положительными числами (минимум 1).', 'danger')
            return render_template('admin/catalog_form.html', entry=entry)

        if watering > 2_000_000_000 or harvest > 2_000_000_000:
            flash('Слишком большое значение. Введите разумное число.', 'danger')
            return render_template('admin/catalog_form.html', entry=entry)

        entry.crop_name = request.form['crop_name']
        entry.variety = request.form['variety']
        entry.watering_interval_days = watering
        entry.days_to_harvest = harvest
        entry.description = request.form.get('description', '')
        entry.emoji = request.form.get('emoji', '🌱')
        db.session.commit()
        flash('Запись обновлена.', 'success')
        return redirect(url_for('admin.catalog'))
    return render_template('admin/catalog_form.html', entry=entry)


@admin_bp.route('/catalog/<int:entry_id>/delete', methods=['POST'])
@login_required
@admin_required
def catalog_delete(entry_id):
    entry = CropCatalog.query.get_or_404(entry_id)
    db.session.delete(entry)
    db.session.commit()
    flash('Запись удалена.', 'info')
    return redirect(url_for('admin.catalog'))


@admin_bp.route('/stats')
@login_required
@admin_required
def stats():
    users = User.query.all()
    data = []
    for u in users:
        seeds = Seed.query.filter_by(user_id=u.id).count()
        plantings = Planting.query.filter_by(user_id=u.id).count()
        data.append({'user': u, 'seeds': seeds, 'plantings': plantings})
    return render_template('admin/stats.html', data=data)