import requests
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError

from app import db
from app.models import User
from app.forms import RegisterForm, LoginForm

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Пользователь с таким email уже зарегистрирован. Попробуйте войти или используйте другой email.', 'warning')
            return redirect(url_for('auth.register'))

        user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data)
        )
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash('Пользователь с таким email уже зарегистрирован. Попробуйте войти или используйте другой email.', 'warning')
            return redirect(url_for('auth.register'))

        flash('Регистрация прошла успешно! Теперь можно войти.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password_hash and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            flash(f'Добро пожаловать, {user.username}!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Неверный email или пароль', 'danger')

    return render_template('login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы успешно вышли из аккаунта', 'info')
    return redirect(url_for('main.index'))


# ==================== YANDEX OAUTH ====================

@auth.route('/yandex/login')
def yandex_login():
    """Перенаправляет пользователя на страницу авторизации Яндекс."""
    client_id = current_app.config['YANDEX_CLIENT_ID']
    if not client_id:
        flash('Yandex OAuth не настроен. Укажите YANDEX_CLIENT_ID в .env', 'warning')
        return redirect(url_for('auth.login'))

    redirect_uri = current_app.config['YANDEX_REDIRECT_URI']
    yandex_auth_url = (
        f"https://oauth.yandex.ru/authorize?"
        f"response_type=code"
        f"&client_id={client_id}"
        f"&redirect_uri={redirect_uri}"
        f"&force_confirm=yes"
    )
    return redirect(yandex_auth_url)


@auth.route('/yandex/callback')
def yandex_callback():
    """Обрабатывает callback от Яндекс OAuth."""
    code = request.args.get('code')
    if not code:
        flash('Ошибка авторизации через Яндекс', 'danger')
        return redirect(url_for('auth.login'))

    client_id = current_app.config['YANDEX_CLIENT_ID']
    client_secret = current_app.config['YANDEX_CLIENT_SECRET']

    # Обмениваем код на токен
    try:
        token_response = requests.post(
            'https://oauth.yandex.ru/token',
            data={
                'grant_type': 'authorization_code',
                'code': code,
                'client_id': client_id,
                'client_secret': client_secret,
            },
            timeout=10
        )
        token_data = token_response.json()
        access_token = token_data.get('access_token')

        if not access_token:
            flash('Не удалось получить токен от Яндекса', 'danger')
            return redirect(url_for('auth.login'))

        # Получаем данные пользователя
        user_response = requests.get(
            'https://login.yandex.ru/info',
            headers={'Authorization': f'OAuth {access_token}'},
            params={'format': 'json'},
            timeout=10
        )
        user_data = user_response.json()

        yandex_id = str(user_data.get('id'))
        email = user_data.get('default_email', '')
        display_name = user_data.get('display_name', user_data.get('login', 'Пользователь'))

        # Ищем пользователя по yandex_id
        user = User.query.filter_by(yandex_id=yandex_id).first()

        if not user:
            # Ищем по email
            user = User.query.filter_by(email=email).first()
            if user:
                # Привязываем Яндекс ID к существующему аккаунту
                user.yandex_id = yandex_id
            else:
                # Создаём нового пользователя (ник не обязан быть уникальным)
                user = User(
                    username=display_name,
                    email=email,
                    yandex_id=yandex_id,
                    password_hash=None
                )
                db.session.add(user)

            db.session.commit()

        login_user(user)
        flash(f'Добро пожаловать, {user.username}! (через Яндекс)', 'success')
        return redirect(url_for('main.dashboard'))

    except Exception as e:
        print(f"Yandex OAuth error: {e}")
        flash('Ошибка авторизации через Яндекс. Попробуйте ещё раз.', 'danger')
        return redirect(url_for('auth.login'))
