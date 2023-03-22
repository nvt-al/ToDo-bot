from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user

from webapp.generate_fake_data import generate
from webapp.generate_fake_data.forms import GenerateDataForm

blueprint = Blueprint("generate_fake_data", __name__, url_prefix="/fake")


@blueprint.route("/")
def fake_data():
    title = "Генерация тестовых данных"
    login_form = GenerateDataForm()
    return render_template("generate_fake_data/fake.html", page_title=title, form=login_form)


@blueprint.route("/process-generation", methods=["POST"])
def process_generation_data():
    form = GenerateDataForm()
    if form.is_submitted():
        generate.generate_fake_data()
    return redirect(url_for("generate_fake_data.fake_data"))
