from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, Length, Optional

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class EditUserForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired(),Length(max=100)])
    age = IntegerField('Age', validators=[Optional()])
    gender = SelectField('Gender', choices=[('', 'Select'), ('male', 'Male'), ('female', 'Female'), ('other', 'Other')], validators=[Optional()])
    height = FloatField('Height (cm)', validators=[Optional()])
    weight = FloatField('Weight (kg)', validators=[Optional()])
    submit = SubmitField('Update Information')
    # Add fields for editing user information
