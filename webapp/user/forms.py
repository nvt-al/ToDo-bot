from flask_wtf import FlaskForm
from wtforms import BooleanField, EmailField, PasswordField, StringField, SubmitField, TimeField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from webapp.user.models import User


class LoginForm(FlaskForm):
    username = StringField(
        "Имя пользователя", validators=[DataRequired()], render_kw={"class": "form-control"}
    )
    password = PasswordField(
        "Пароль", validators=[DataRequired()], render_kw={"class": "form-control"}
    )
    submit = SubmitField("Отправить", render_kw={"class": "btn btn-primary"})
    remember_me = BooleanField(
        "Запомнить меня", default=True, render_kw={"class": "form-check-input"}
    )


class RegistrationForm(FlaskForm):
    username = StringField(
        "Имя пользователя", validators=[DataRequired()], render_kw={"class": "form-control"}
    )
    email = EmailField(
        "Email", validators=[DataRequired(), Email()], render_kw={"class": "form-control"}
    )
    password = PasswordField(
        "Пароль", validators=[DataRequired()], render_kw={"class": "form-control"}
    )
    password2 = PasswordField(
        "Повторите пароль",
        validators=[DataRequired(), EqualTo("password")],
        render_kw={"class": "form-control"},
    )
    submit = SubmitField("Отправить!", render_kw={"class": "btn btn-primary"})

    def validate_username(self, username):
        users_count = User.query.filter_by(username=username.data).count()
        if users_count > 0:
            raise ValidationError("Пользователь c таким именем уже зарегистрирован")

    def validate_email(self, email):
        users_count = User.query.filter_by(email=email.data).count()
        if users_count > 0:
            raise ValidationError("Пользователь c такой электронной почтой уже зарегистрирован")


class SettingsForm(FlaskForm):
    telegram_user = StringField("Telegram", render_kw={"class": "form-control"})
    default_reminder_time = TimeField("Время напоминаний", render_kw={"class": "form-control"})
    time_start_new_day = TimeField("Начало нового дня", render_kw={"class": "form-control"})
    week_report = BooleanField(
        "Отправлять отчёт за неделю", render_kw={"class": "form-check-input"}
    )
    month_report = BooleanField(
        "Отправлять отчёт за месяц", render_kw={"class": "form-check-input"}
    )
    submit = SubmitField("Сохранить", render_kw={"class": "btn btn-primary"})
