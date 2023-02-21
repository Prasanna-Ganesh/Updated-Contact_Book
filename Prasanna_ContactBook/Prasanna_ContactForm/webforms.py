from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired,Length,Email,ValidationError
from Prasanna_ContactForm.models import Contact

class AdduserForm(FlaskForm):
    name= StringField('name', validators=[DataRequired(),Length(min=3,max=20)])
    email= StringField('email',validators= [DataRequired(), Email()])
    phno = StringField('phno',validators = [DataRequired(),Length(min=10,max=10)])
    submit = SubmitField('Submit')
    def validate_name(self,name):
        user = Contact.query.filter_by(name=name.data).first()
        if user:
            raise ValidationError('Contact Name already Exists. Please use different one.')

    def validate_email(self,email):
        user =Contact.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

    def validate_phno(self,phno):
        user = Contact.query.filter_by(phno=phno.data).first()
        if user:
            raise ValidationError('That Contact is already Saved. Please choose a different one.')

class SearchForm(FlaskForm):
    searched = StringField("Searched",validators=[DataRequired()])
    submit = SubmitField("Submit")



