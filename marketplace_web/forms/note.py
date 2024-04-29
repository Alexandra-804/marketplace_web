from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, DateTimeLocalField, SelectField
from wtforms.validators import DataRequired, Length

from forms import category

class NoteForm(FlaskForm):
    title = StringField('Наименование', validators=[DataRequired(), Length(min=4, max=25)])
    price = StringField('Цена', validators=[DataRequired()])
    user_id = StringField('Имя пользователя', validators=[DataRequired()])
    amount = StringField('Количество', validators=[DataRequired()])
    about = StringField('Описание', validators=[DataRequired()])
    category_id = SelectField("Категория", validate_choice=False, choices=[])
    submit = SubmitField('Добавить')

    def __init__(self, *args, **kwargs):
        super(NoteForm, self).__init__(*args, **kwargs)
        if kwargs.get('categories', False):
            self.category_id.choices = list(map(lambda x: (x.id, x.name),kwargs['categories']))