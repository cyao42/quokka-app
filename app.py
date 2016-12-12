from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
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
    global isStudent
    form = forms.UserLoginFormFactory.form()
    user = currentuser
    if form.validate_on_submit():
        try:
            isStudent = True
            user = db.session.query(models.Student)\
                            .filter(models.Student.email == form.email.data).first()
            if user:
                isStudent = True
                if user.password == form.password.data:
                    currentuser = user
                    form.errors.pop('database', None)
                    return redirect('/profile')
                else:
                    return render_template('login.html', form=form, user=None, msg="Incorrect password!")
            else:
                user = db.session.query(models.Professor)\
                            .filter(models.Professor.email == form.email.data).first()
                if user:
                    isStudent = False
                    if user.password == form.password.data:
                        currentuser = user
                        form.errors.pop('database', None)
                        return redirect('/profile')
                    else:
                        return render_template('login.html', form=form, user=None, msg="Incorrect password!")
                else:
                    return render_template('login.html', form=form, user=None, msg="No user with that email")
        except BaseException as e:
            form.errors['database'] = str(e)
            return render_template('login.html', form=form, user=currentuser)
    else:
        return render_template('login.html', form=form, user=currentuser)

@app.route('/<sectionid>/new-group', methods=['GET', 'POST'])
def new_group(sectionid):
    global currentuser
    if not currentuser:
        return redirect('/')
    
    assignments = db.session.query(models.ProjectAssignment)\
                      .join(models.AssignedTo)\
                      .filter(models.AssignedTo.section_id == sectionid)
    form = forms.GroupNewFormFactory.form(assignments)
    if form.validate_on_submit():
        try:
            form.errors.pop('database', None)
            models.Groups.addNew(form.name.data, sectionid, form.assign.data, currentuser)
            return redirect('/profile')
        except BaseException as e:
            form.errors['database'] = str(e)
            return render_template('new-group.html', form=form, sectionid=sectionid)
    else:
        return render_template('new-group.html', form=form, sectionid=sectionid)

@app.route('/profile')
def user():
    global currentuser
    if(currentuser):
        groups = db.session.query(models.Groups).\
                 join(models.MemberOf).\
                 filter(models.MemberOf.u_id == currentuser.u_id).all()
        classes = db.session.query(models.Section, models.Course.course_name, models.Course.course_pre, models.Section.section_id, models.Section.course_semester, models.Section.university_name, models.Section.university_location, models.Section.course_code, models.Section.section_number).\
                  join(models.RegisteredWith).\
                  join(models.Course, and_(models.Section.course_code==models.Course.course_code, models.Section.course_semester==models.Course.course_semester, models.Section.university_name==models.Course.university_name, models.Section.university_location==models.Course.university_location)).\
                  filter(models.RegisteredWith.u_id == currentuser.u_id).all()
        return render_template('user.html', user=currentuser, isStudent=isStudent, groups=groups, classes=classes)
    else:
        return redirect('/')

@app.route('/register-class', methods=['GET', 'POST'])
def register_class():
    global currentuser
    if not currentuser:
        return redirect('/')

    form = forms.ClassRegisterFormFactory.form()
    if form.validate_on_submit():
        try:
            form.errors.pop('database', None)
            section = db.session.query(models.Section)\
                      .filter(models.Section.section_id == form.section_code.data).first()
            if section:
                models.RegisteredWith.addNew(currentuser.u_id, section.section_id)
                return redirect('/profile')
            else:
                return render_template('register-class.html', form=form, msg="No class found with that code!")
        except BaseException as e:
            form.errors['database'] = str(e)
            return render_template('register-class.html', form=form)
    else:
        return render_template('register-class.html', form=form)

@app.route('/create-class', methods=['GET', 'POST'])
def create_class():
    global currentuser
    if not currentuser:
        return redirect('/')
    
    universities = db.session.query(models.University).all()
    form = forms.ClassCreateFormFactory.form(universities)
    if form.validate_on_submit():
        try:
            form.errors.pop('database', None)
            university = db.session.query(models.University)\
                .filter(models.University.university_name == form.university.data).first()
            if university:
                models.Course.addNew(form.course_code.data,form.course_semester.data,university.university_name,university.university_location,form.course_name.data,form.course_pre.data)
                startSect = db.session.query(models.Section).count()+1
                for x in xrange(1,form.num_sect.data+1):
                    models.Section.addNew(form.course_code.data,form.course_semester.data,university.university_name,university.university_location,x)
                endSect = db.session.query(models.Section).count()
                for s in xrange(startSect,endSect+1):
                    models.RegisteredWith.addNew(currentuser.u_id, s)
                return redirect('/profile')
            else:
                return render_template('create-class.html', form=form)
        except BaseException as e:
            form.errors['database'] = str(e)
            return render_template('create-class.html', form=form)
    else:
        return render_template('create-class.html', form=form)

@app.route('/create-university', methods=['GET', 'POST'])
def create_university():
    global currentuser
    if not currentuser:
        return redirect('/')
    
    form = forms.UniversityCreateFormFactory.form()
    if form.validate_on_submit():
        try:
            form.errors.pop('database', None)
            models.University.addNew(form.u_name.data,form.u_loc.data)
            return redirect('/create-class')
        except BaseException as e:
            form.errors['database'] = str(e)
            return render_template('create-university.html', form=form)
    else:
        return render_template('create-university.html', form=form)

@app.route('/register-user/', methods=['GET', 'POST'])
def register_user():
    global currentuser
    form = forms.UserRegisterFormFactory.form()
    if form.validate_on_submit():
        try:
            form.errors.pop('database', None)
            email_check = db.session.query(models.Users)\
                          .filter(models.Users.email == form.email.data).first()
            if(email_check):
                return render_template('register.html', form=form, msg="User with that email already exists")
            else:
                models.Users.addNew(form.name.data, form.phone.data, form.email.data, form.user_type.data, form.password.data)
                currentuser = db.session.query(models.Users).filter(models.Users.email == form.email.data).first()
                return redirect('/profile')
        except BaseException as e:
            form.errors['database'] = str(e)
            return render_template('register.html', form=form)
    else:
        return render_template('register.html', form=form)

@app.route('/feed/<id>')
def classfeed(id):
    section = db.session.query(models.Section)\
        .filter(models.Section.section_id == id).all()
    course_code = section.course_code
    assignments = db.session.query(models.ProjectAssignment)\
                    .join(models.AssignedTo)\
                    .join(models.Section)\
                    .filter(models.Section.section_id == id)
    return render_template('classfeed.html', section = section, assignments = assignments)

@app.route('/classfeed/', methods=['GET', 'POST'])
def getPosts(): 
    assignment_id = request.form.get('selected_assignment')
    assignment = db.session.query(models.ProjectAssignment)\
        .filter(models.ProjectAssignment.assignment_id == assignment_id).all()
    posts = assignment.posts
    return render_template('classfeed.html', posts=posts, assignment=assignment)

@app.route('/membersof/<g_id>')
def membersOf(g_id):
    member = db.session.query(models.Student)\
       .join(models.MemberOf, (models.Student.u_id == models.MemberOf.u_id))\
       .filter(models.MemberOf.g_id == g_id).all()
    group = db.session.query(models.Groups)\
       .filter(models.Groups.g_id == g_id).first()
    return render_template('membersof.html', member=member, group=group)

@app.template_filter('pluralize')
def pluralize(number, singular='', plural='s'):
    return singular if number in (0, 1) else plural

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
