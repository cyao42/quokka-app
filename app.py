from flask import Flask, render_template, redirect, url_for
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
    form = forms.UserLoginFormFactory.form()
    user = currentuser
    if form.validate_on_submit():
        try:
            user = db.session.query(models.Users)\
                            .filter(models.Users.email == form.email.data).first()
            if user:
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
        classes = db.session.query(models.Section)\
                  .join(models.RegisteredWith)\
                 .filter(models.RegisteredWith.u_id == currentuser.u_id).all()
        return render_template('user.html', user=currentuser, groups=groups, classes=classes)
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

@app.route('/register-user/', methods=['GET', 'POST'])
def register_user():
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
def classfeed(id):
    course = db.session.query(models.Course)\
       .filter(models.Class.id == id).one()
    assignments = models.Course.getAssignments(course.course_code) 
    return render_template('classfeed.html', course=course)

def getPosts(assignment): 
    posts = assignment.posts
    return render_template('classfeed-posts.html', posts=posts, assignment=assignment)

@app.route('/mygroups/')
def myGroups():
    return render_template('mygroups.html')

@app.route('/myclasses/')
def myClasses():
    return render_template('myclasses.html')

@app.route('/membersof/<g_id>')
def membersOf(g_id):
    member = db.session.query(models.Student)\
       .join(models.MemberOf, (models.Student.u_id == models.MemberOf.u_id))\
       .filter(models.MemberOf.g_id == g_id).all()
    return render_template('membersof.html', member=member)

@app.template_filter('pluralize')
def pluralize(number, singular='', plural='s'):
    return singular if number in (0, 1) else plural

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
