from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class TaskForm(FlaskForm):
    title = StringField("Title:", validators=[DataRequired()])
    description = TextAreaField("Description:")
    complete = BooleanField("Complete:")
    submit = SubmitField("Submit")
