from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField, SelectField, PasswordField
from wtforms.validators import DataRequired


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
            phone = StringField(default='')
            email = StringField(default='')
            user_type = SelectField('User Type', choices=[('pro', 'Professor'), ('stu', 'Student')])
        return F()

class ClassRegisterFormFactory:
    @staticmethod
    def form():
        class F(FlaskForm):
            section_code = StringField(default='')
        return F()
