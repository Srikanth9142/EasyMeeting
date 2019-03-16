
from flask_wtf import FlaskForm 
from flask_wtf.file import FileField,FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField,TextAreaField,DateTimeField
from wtforms.validators import DataRequired,ValidationError, Length, Email, EqualTo
from wtforms.fields.html5 import DateField
#import  User

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

   # def validate_username(self,username):
        #user = User.query.filter_by(username=username.data).first()
        #if user:
           # raise ValidationError('User Name Exist')
    
   # def validate_email(self,email):
    #    user = User.query.filter_by(email=email.data).first()
    #    if user:
     #       raise ValidationError('Email  Exist')#


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')

    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture',validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update')


class AddMeetForm(FlaskForm):
    title = StringField('Title of meeting',validators=[DataRequired(),Length(min=2,max=40)])
    meet_person = StringField('Email',validators=[Email()])
    date = DateField('Date of Meeting',validators=[DataRequired()])
    time = StringField('Time of meeting',validators=[DataRequired()])
    content = TextAreaField('content',validators=[DataRequired()])
    submit = SubmitField('Add Meeting')

