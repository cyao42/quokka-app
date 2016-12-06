from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField, SelectField, PasswordField
from wtforms.validators import DataRequired

class GroupNewFormFactory:
    @staticmethod
    def form(sections, assignments):
        class F(FlaskForm):
            name = StringField(default='')
            course_options = [(section, section.course_code) for section in sections]
            course = SelectField('Course', choices=course_options)
            # if course.data:
            #     assignment = SelectField('Assignment', choices)
            # assignment = SelectField('')

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
