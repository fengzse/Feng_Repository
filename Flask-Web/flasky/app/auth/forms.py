from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 120), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 120), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(1, 64),
                                                   Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                          'Usernames must have only letters, '
                                                          'numbers, dots or underscores')])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password_confirm',
                                                                             message='Passwords must match!')])
    password_confirm = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), EqualTo('new_password_confirm',
                                                                                     message='Passwords must match!')])
    new_password_confirm = PasswordField('Confirm New Password', validators=[DataRequired()])
    submit = SubmitField('Change password')


class ResetPassword(FlaskForm):
    reset_password = PasswordField('New Password', validators=[DataRequired(), EqualTo('reset_password_confirm',
                                                                                       message='Passwords must match!')])
    reset_password_confirm = PasswordField('Confirm New Password', validators=[DataRequired()])
    submit = SubmitField('Reset password')


class ResetPasswordRequest(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 120), Email()])
    submit = SubmitField('Reset Password')


class ChangeEmailForm(FlaskForm):
    newemail = StringField('New Email', validators=[DataRequired(), Length(1, 120), Email()])
    password = PasswordField('Enter your password', validators=[DataRequired()])
    submit = SubmitField('Update Email Address ')

    def validate_newemail(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')
