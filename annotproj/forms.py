from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,\
     TextAreaField, HiddenField, RadioField, SelectField, IntegerField
from wtforms.validators import InputRequired, Length, Email, EqualTo, ValidationError, DataRequired
from wtforms.widgets import HiddenInput
from annotproj.models import User
from annotproj.languages import language_codes as lc

ll = [("none", "None"), ("A1", "Beginner, A1"), ("A2", "A2"), ("B1", "Intermediate, B1"), ("B2","B2"),("C1", "Advanced, C1"), ("C2", "C2"), ("Native", "Native")]


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    native_language = SelectField('Native Language', choices = lc, validators=[InputRequired()])
    german_level = SelectField('German Level', choices = ll, validators=[InputRequired()])
    english_level = SelectField('English Level', choices = ll, validators=[InputRequired()])
    accepted_agreement = BooleanField('I have read and agreed to the privacy statement:', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class AnnotationForm(FlaskForm):
    annotationfield = HiddenField('annotationfield', validators=[InputRequired()])
    timestarted = IntegerField('timestarted', validators=[InputRequired()], widget=HiddenInput())
    key = IntegerField('key', validators=[InputRequired()], widget=HiddenInput())
    userchoice = HiddenField('userchoice')
    submit = SubmitField('Save Annotation')
    timesubmitted = IntegerField('timesubmitted',validators=[InputRequired()], widget=HiddenInput())
    clicks = IntegerField('clicks', validators=[InputRequired()], widget=HiddenInput())
    keystrokes = IntegerField('keystrokes', validators=[InputRequired()], widget=HiddenInput())
    timepaused = IntegerField('timepaused', validators=[InputRequired()], widget=HiddenInput())

class EvalForm(FlaskForm):
    better = IntegerField('better', validators=[InputRequired()], widget=HiddenInput())
    timestarted = IntegerField('timestarted', validators=[InputRequired()], widget=HiddenInput())
    timesubmitted = IntegerField('timesubmitted',validators=[InputRequired()], widget=HiddenInput())
    clicks = IntegerField('clicks', validators=[InputRequired()], widget=HiddenInput())
    timepaused = IntegerField('timepaused', validators=[InputRequired()], widget=HiddenInput())
    key = IntegerField('key', validators=[InputRequired()], widget=HiddenInput())
    submit = SubmitField('Save Evaluation')
    minimum = 0
    maximum = 5

    #def validate_better(form, field):
    #    if field.data > maximum or field.data < minimum:
    #        raise ValidationError("The selected value is outside of the allowed range")

