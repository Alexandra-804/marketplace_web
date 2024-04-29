from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField
from wtforms.validators import DataRequired, Length


class CategoryForm(FlaskForm):
    name = StringField('Наименование категории', validators=[DataRequired(), Length(min=4, max=25)])
    submit = SubmitField('Добавить')