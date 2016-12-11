from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField, SelectField, PasswordField
from wtforms.validators import DataRequired, Length, Required, EqualTo


class GroupNewFormFactory:
    @staticmethod
    def form(assignments):
        class F(FlaskForm):
            name = StringField(default='')
            assign_options = [("none", "Study Group")]
            assign_options.extend([(str(assign.assignment_id), assign.assignment_id) for assign in assignments])
            assign = SelectField('Assignment', choices=assign_options)
        return F()

class UserLoginFormFactory:
    @staticmethod
    def form():
        class F(FlaskForm):
            email = StringField(default='')
            password = PasswordField(default='')
        return F()

class UserRegisterFormFactory:
    @staticmethod
    def form():
        class F(FlaskForm):
            name = StringField(default='')
            password = PasswordField('Password', [Required(), Length(8, 256), EqualTo('confirm_pw', message="Passwords don't match")])
            confirm_pw = PasswordField('Confirm Password', [Required()])
            phone = StringField('Phone Number')
            email = StringField('Email', [Required()])
            user_type = SelectField('User Type', choices=[('stu', 'Student'), ('pro', 'Professor')])
        return F()

class ClassRegisterFormFactory:
    @staticmethod
    def form():
        class F(FlaskForm):
            section_code = StringField(default='')
        return F()
