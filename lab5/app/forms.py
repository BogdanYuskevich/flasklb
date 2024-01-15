from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField("Username",
                           validators=[
                               DataRequired(message="Це поле потребує заповнення")
                           ])
    password = PasswordField("Password",
                             validators=[
                                 DataRequired(message="Це поле потребує заповнення"),
                                 Length(min=4, max=10)
                             ])
    remember = BooleanField("Запам'ятати мене")
    submit = SubmitField("Логін")


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField("Старий пароль",
                                 validators=[
                                     DataRequired(),
                                     Length(min=4, max=10)
                                 ])
    new_password = PasswordField("Новий пароль",
                                 validators=[
                                     DataRequired(),
                                     Length(min=4, max=10)
                                 ])
    confirm_password = PasswordField("Підтвердити новий пароль",
                                     validators=[
                                         DataRequired(),
                                         Length(min=4, max=10)
                                     ])
    submit = SubmitField("OK")
