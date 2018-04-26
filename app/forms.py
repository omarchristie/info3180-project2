from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, TextAreaField, IntegerField
from wtforms.validators import InputRequired, Email
from wtforms.fields.html5 import DateField
from flask_wtf.file import FileField, FileAllowed, FileRequired


class LoginForm(FlaskForm):
    userName = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    
class RegistrationForm(FlaskForm):
    userName= StringField('Username', validators=[InputRequired()])
    password= PasswordField('Password', validators=[InputRequired()])
    firstName=StringField('FirstName', validators=[InputRequired()])
    lastName=StringField('LastName', validators=[InputRequired()])
    email=StringField('Email', validators=[InputRequired(message='Email is required'), Email(message="Only Emails")])
    location=StringField('Location', validators=[InputRequired()])
    biography=TextAreaField('Biography',validators=[InputRequired()])
    proPhoto=FileField('Image', validators=[FileRequired('Please input a file'), FileAllowed(['jpg', 'png'], 'Images only!')])

class newPostForm(FlaskForm):
    photo = FileField('Image', validators=[FileRequired('Please input a file'), FileAllowed(['jpg', 'png'], 'Images only!')])
    caption = TextAreaField('Caption',validators=[InputRequired()])