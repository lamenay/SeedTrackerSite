from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, IntegerField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Optional, ValidationError
import re


def simple_email(form, field):
    """Простая проверка email без внешних зависимостей."""
    if not field.data or '@' not in field.data:
        raise ValidationError('Введите корректный email адрес.')


class RegisterForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), simple_email])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class SeedForm(FlaskForm):
    catalog_id = SelectField('Выберите из справочника', coerce=int, validators=[Optional()])
    crop_name = StringField('Культура', validators=[DataRequired()])
    variety = StringField('Сорт')
    manufacturer = StringField('Производитель')
    purchase_date = DateField('Дата покупки', format='%Y-%m-%d', validators=[Optional()])
    expiry_date = DateField('Срок годности', format='%Y-%m-%d', validators=[Optional()])

    packets_count = IntegerField('Количество пакетиков', default=1)
    seeds_per_packet = IntegerField('Семян в одном пакетике', default=0)

    notes = TextAreaField('Заметки')
    submit = SubmitField('Добавить семена')


class PlantingForm(FlaskForm):
    seed_id = SelectField('Семена', coerce=int, validators=[DataRequired()])
    sowing_date = DateField('Дата посева', format='%Y-%m-%d', validators=[DataRequired()])
    quantity_sown = IntegerField('Количество семян', validators=[DataRequired()])
    location = StringField('Место посадки')
    watering_interval = IntegerField('Интервал полива (дней)', validators=[Optional()])
    days_to_harvest = IntegerField('Дней до урожая', validators=[Optional()])
    notes = TextAreaField('Заметки')
    submit = SubmitField('Посадить')


class UserSettingsForm(FlaskForm):
    city = StringField('Город', validators=[DataRequired()])
    submit = SubmitField('Сохранить')
