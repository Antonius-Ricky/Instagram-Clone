from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, PasswordField, SubmitField, EmailField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min = 4, max = 8)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min = 8)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password", message = "Password must match!")])
    submit = SubmitField("Sign Up")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min = 1)])
    submit = SubmitField("Login")

class EditProfile(FlaskForm):
    username =  StringField("Username", validators=[DataRequired(), Length()])
    bio = TextAreaField("Bio :")
    profile_picture = StringField("Profile picture : ")
    password = password = PasswordField("Password", validators=[DataRequired(), Length(min = 1)])
    Submit = SubmitField("Submit Edit")

class CreatePostForm(FlaskForm):
    post = StringField("Post : ")
    caption = StringField("Caption : ")
    Submit = SubmitField("Post")

class EditPost(FlaskForm):
    post = StringField("Post : ")
    caption = StringField("Caption : ")
    Submit = SubmitField("Submit Edit")

