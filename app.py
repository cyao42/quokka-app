from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import models
import forms

app = Flask(__name__)
app.secret_key = 's3cr3t'
app.config.from_object('config')
db = SQLAlchemy(app, session_options={'autocommit': False})
currentuser = None

@app.route('/', methods=['GET', 'POST'])
def login_user():
    global currentuser
    form = forms.UserLoginFormFactory.form()
    user = currentuser
    if form.validate_on_submit():
        try:
            user = db.session.query(models.Users)\
                          .filter(models.Users.email == form.email.data).first()
            currentuser = user
            form.errors.pop('database', None)
            return redirect('/')
        except BaseException as e:
            form.errors['database'] = str(e)
            return render_template('login.html', form=form, user=currentuser)
    else:
        return render_template('login.html', form=form, user=currentuser)

@app.route('/new-group', methods=['GET', 'POST'])
def new_group():
    global currentuser
    student_sections = db.session.query(models.Section)\
        .filter(models.RegisteredWith.u_id == currentuser.u_id and
            models.RegisteredWith.section_number == models.Section.section_number and
            models.RegisteredWith.course_code == models.Section.course_code and
            models.RegisteredWith.course_semester == models.Section.course_semester and
            models.RegisteredWith.university_name == models.Section.university_name and
            models.RegisteredWith.university_location == models.Section.university_location).all()
    # assignments = db.session.query(models.AssignedTo)\
    #     .filter(student_sections.section_number == models.AssignedTo.section_number and
    #         student_sections.course_code == models.AssignedTo.course_code and 
    #         student_sections.course_semester == models.AssignedTo.course_semester and
    #         student_sections.university_name == models.AssignedTo.university_name and
    #         student_sections.university_location == models.AssignedTo.university_location)
    form = forms.GroupNewFormFactory.form(student_sections)
    if form.validate_on_submit():
        try:
            form.errors.pop('database', None)
            models.SchoolGroup.addNew(form.name.data, form.course.data, currentuser)
            # if form.assignment:
            #     models.ProjectGroup.addNew(form.name, form.Class, form.assignment)
            # else:
            return redirect('/')
        except BaseException as e:
            form.errors['database'] = str(e)
            return render_template('register.html', form=forms.UserLoginFormFactory.form())
    else:
        return render_template('register.html', form=forms.UserLoginFormFactory.form())

@app.route('/user/<id>')
def user(name):
    user = db.session.query(models.User)\
       .filter(models.User.id == id).one()
    return render_template('user.html', user=user)

@app.route('/register/', methods=['GET', 'POST'])
def register():
    print("hit register")
    form = forms.UserRegisterFormFactory.form()
    if form.validate_on_submit():
        try:
            form.errors.pop('database', None)
            models.Users.addNew(form.name.data, form.phone.data,
                                form.email.data, form.user_type.data)
            return redirect('/')
        except BaseException as e:
            form.errors['database'] = str(e)
            return render_template('register.html', form=form)
    else:
        return render_template('register.html', form=form)

@app.route('/classfeed/<id>')
def classfeed():
    classfeed = db.session.query(models.Course)\
       .filter(models.Course.id == id).one()
    return render_template('classfeed.html', classfeed=classfeed)

@app.template_filter('pluralize')
def pluralize(number, singular='', plural='s'):
    return singular if number in (0, 1) else plural

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
