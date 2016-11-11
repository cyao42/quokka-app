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
            user = db.session.query(models.SchoolUser)\
                          .filter(models.SchoolUser.email == form.email.data).first()
            currentuser = user
            form.errors.pop('database', None)
            return redirect('/')
        except BaseException as e:
            form.errors['database'] = str(e)
            return render_template('all-drinkers.html', form=form, user=currentuser)
    else:
        return render_template('all-drinkers.html', form=form, user=currentuser)

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
            #     models.ProjectGroup.addNew(form.name, form.course, form.assignment)
            # else:
            return redirect('/')
        except BaseException as e:
            form.errors['database'] = str(e)
            return render_template('new-drinker.html', form=forms.UserLoginFormFactory.form())
    else:
        return render_template('new-drinker.html', form=forms.UserLoginFormFactory.form())

@app.route('/drinker/<name>')
def drinker(name):
    drinker = db.session.query(models.Drinker)\
        .filter(models.Drinker.name == name).one()
    return render_template('drinker.html', drinker=drinker)

@app.route('/edit-drinker/<name>', methods=['GET', 'POST'])
def edit_drinker(name):
    drinker = db.session.query(models.Drinker)\
        .filter(models.Drinker.name == name).one()
    beers = db.session.query(models.Beer).all()
    bars = db.session.query(models.Bar).all()
    form = forms.DrinkerEditFormFactory.form(drinker, beers, bars)
    if form.validate_on_submit():
        try:
            form.errors.pop('database', None)
            models.Drinker.edit(name, form.name.data, form.address.data,
                                form.get_beers_liked(), form.get_bars_frequented())
            return redirect(url_for('drinker', name=form.name.data))
        except BaseException as e:
            form.errors['database'] = str(e)
            return render_template('edit-drinker.html', drinker=drinker, form=form)
    else:
        return render_template('edit-drinker.html', drinker=drinker, form=form)

@app.route('/new-drinker/', methods=['GET', 'POST'])
def new_drinker():
    beers = db.session.query(models.Beer).all()
    bars = db.session.query(models.Bar).all()
    form = forms.DrinkerNewFormFactory.form(beers, bars)
    if form.validate_on_submit():
        try:
            form.errors.pop('database', None)
            models.Drinker.addNew(form.name.data, form.address.data,
                                form.get_beers_liked(), form.get_bars_frequented())
            return redirect(url_for('drinker', name=form.name.data))
        except BaseException as e:
            form.errors['database'] = str(e)
            return render_template('new-drinker.html', form=form)
    else:
        return render_template('new-drinker.html', form=form)

@app.route('/new-user/', methods=['GET', 'POST'])
def new_user():
    form = forms.UserNewFormFactory.form()
    if form.validate_on_submit():
        try:
            form.errors.pop('database', None)
            models.SchoolUser.addNew(form.name.data, form.phone.data,
                                form.email.data, form.user_type.data)
            return redirect('/')
        except BaseException as e:
            form.errors['database'] = str(e)
            return render_template('new-user.html', form=form)
    else:
        return render_template('new-user.html', form=form)

@app.template_filter('pluralize')
def pluralize(number, singular='', plural='s'):
    return singular if number in (0, 1) else plural

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
