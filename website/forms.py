from flask.helpers import flash

# from .api import *
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, form
from wtforms.validators import DataRequired, Length, Email, ValidationError, EqualTo
from .models import User
from . import db
import logging
from flask_login import current_user


class UpdateAccountForm(FlaskForm):
   fullName = StringField('Fullname', validators=[DataRequired(), Length(min=2, max=20)])
   email = StringField('Email', validators=[DataRequired(), Email()] ) 
   picture = FileField('update profile picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
   submit = SubmitField("Update")

   def validate_fullName (self, field):
      if field.data != current_user.full_name:
         user = User.query.filter_by(full_name=field.data).first()
         if user:
            #    print("VALIDATION FAILED")
               # print(user)
            return {"That full_name is taken" :  "Please choose different one"},  422
               
      
   def validate_email (self, field):
      if field.data != current_user.email:
         user = User.query.filter_by(email=field.data).first()
         if user:
            #    print("VALIDATION FAILED")
            return {"That email is taken" : " Please choose different one"}, 422
               

