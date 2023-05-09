from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TimeField
from wtforms.validators import DataRequired, Length


class TaskTemplateForm(FlaskForm):
    name = StringField(
        "Краткое название задачи: ",
        validators=[
            DataRequired(),
            Length(min=1, max=100, message="Текст должен быть от 1 до 100 символов"),
        ],
        render_kw={"class": "form-control"},
    )
    description = StringField("Описание задачи: ", render_kw={"class": "form-control"})
    to_time = TimeField("Время напоминания", format="%H:%M", render_kw={"class": "form-control"})
    submit = SubmitField("Создать", render_kw={"class": "btn btn-primary"})
