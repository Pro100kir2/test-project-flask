from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo

class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=8, max=12)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=12)])
    birth_date = DateField('Birth Date', format='%d.%m.%Y', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('man', 'Man'), ('woman', 'Woman'), ('other', 'Other')], validators=[DataRequired()])
    full_name = StringField('Full Name', validators=[DataRequired(), Length(max=24)])

class LoginForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
