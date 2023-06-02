from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_user, logout_user

from webapp.models import db
from webapp.user.forms import LoginForm, RegistrationForm, SettingsForm
from webapp.user.models import User

blueprint = Blueprint("user", __name__, url_prefix="/user")


@blueprint.route("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("tasks.index"))
    title = "Авторизация"
    login_form = LoginForm()
    return render_template("user/login.html", page_title=title, form=login_form)


@blueprint.route("/process-login", methods=["POST"])
def process_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Вы вошли на сайт")
            return redirect(url_for("tasks.index"))

    flash("Неправильное имя пользователя или пароль")
    return redirect(url_for("user.login"))


@blueprint.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("tasks.index"))


@blueprint.route("/register")
def register():
    if current_user.is_authenticated:
        return redirect(url_for("tasks.index"))
    form = RegistrationForm()
    title = "Регистрация"
    return render_template("user/registration.html", page_title=title, form=form)


@blueprint.route("/process-reg", methods=["POST"])
def process_reg():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash("Вы успешно зарегистрировались!")
        return redirect(url_for("user.login"))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(
                    'Ошибка в поле "{}": - {}'.format(
                        getattr(form, field).label.text, error
                    )
                )
        return redirect(url_for("user.register"))


@blueprint.route("/settings")
def settings():
    if not current_user.is_authenticated:
        return redirect(url_for("user.login"))
    settings_form = SettingsForm(
        telegram_user=current_user.telegram_user,
        default_reminder_time=current_user.default_reminder_time,
        time_start_new_day=current_user.time_start_new_day,
        week_report=current_user.week_report,
        month_report=current_user.month_report,
    )
    title = "Настройки"
    return render_template("user/settings.html", page_title=title, form=settings_form)


@blueprint.route("/process-save-settings", methods=["POST"])
def process_save_settings():
    settings_form = SettingsForm()
    my_user = User.query.filter_by(id=current_user.id).first()
    if settings_form.validate_on_submit():
        my_user.telegram_user = settings_form.telegram_user.data
        my_user.default_reminder_time = settings_form.default_reminder_time.data
        my_user.time_start_new_day = settings_form.time_start_new_day.data
        my_user.week_report = settings_form.week_report.data
        my_user.month_report = settings_form.month_report.data
        db.session.commit()
        flash("Настройки успешно сохранены!")
    else:
        for field, errors in settings_form.errors.items():
            for error in errors:
                flash(
                    'Ошибка в поле "{}": - {}'.format(
                        getattr(settings_form, field).label.text, error
                    )
                )
    return redirect(url_for("user.settings"))
