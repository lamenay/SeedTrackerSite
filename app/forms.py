from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, IntegerField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Optional, ValidationError, NumberRange
from datetime import date
import re


def simple_email(form, field):
    """Простая проверка email без внешних зависимостей."""
    if not field.data or '@' not in field.data:
        raise ValidationError('Введите корректный email адрес.')


MAX_SEED_VALUE = 2_000_000_000  # Максимальное значение для SQLite INTEGER


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

    packets_count = IntegerField('Количество пакетиков', default=1,
                                 validators=[NumberRange(min=1, max=MAX_SEED_VALUE,
                                                         message=f'Количество пакетиков должно быть от 1 до {MAX_SEED_VALUE:,}')])
    seeds_per_packet = IntegerField('Семян в одном пакетике', default=1,
                                    validators=[NumberRange(min=1, max=MAX_SEED_VALUE,
                                                            message=f'Количество семян должно быть от 1 до {MAX_SEED_VALUE:,}')])

    notes = TextAreaField('Заметки')
    submit = SubmitField('Добавить семена')

    def validate_purchase_date(self, field):
        if field.data and field.data > date.today():
            raise ValidationError('Дата покупки не может быть в будущем.')

    def validate_expiry_date(self, field):
        if field.data and field.data <= date.today():
            raise ValidationError('Эти семена уже просрочены! Нельзя добавить семена с истёкшим сроком годности.')


class PlantingForm(FlaskForm):
    seed_id = SelectField('Семена', coerce=int, validators=[DataRequired()])
    sowing_date = DateField('Дата посева', format='%Y-%m-%d', validators=[DataRequired()])
    quantity_sown = IntegerField('Количество семян',
                                 validators=[DataRequired(),
                                             NumberRange(min=1, max=MAX_SEED_VALUE,
                                                         message=f'Количество семян должно быть от 1 до {MAX_SEED_VALUE:,}')])
    location = StringField('Место посадки')
    watering_interval = IntegerField('Интервал полива (дней)', validators=[Optional(),
                                     NumberRange(min=1, message='Интервал полива должен быть положительным числом.')])
    days_to_harvest = IntegerField('Дней до урожая', validators=[Optional(),
                                   NumberRange(min=1, message='Дней до урожая должно быть положительным числом.')])
    notes = TextAreaField('Заметки')
    submit = SubmitField('Посадить')


class UserSettingsForm(FlaskForm):
    city = StringField('Город', validators=[DataRequired()])
    submit = SubmitField('Сохранить')
