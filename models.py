from sqlalchemy import sql, orm, join
from sqlalchemy.sql import text 
from app import db
import datetime

class Users(db.Model):
    __tablename__ = 'users'
    u_id = db.Column('u_id', db.Integer(), primary_key=True)
    name = db.Column('name', db.String(256))
    phone = db.Column('phone', db.String(15))
    email = db.Column('email', db.String(256))
    password = db.Column('password', db.String(256))
    @staticmethod
    def addNew(name, phone, email, user_type, password):
        try:
            u_id = db.session.query(Users).count()+1
            db.session.execute('INSERT INTO users VALUES(:u_id, :name, :phone, :email, :password)',
                               dict(u_id=u_id, name=name, phone=phone, email=email, password=password))
            if user_type == 'pro':
                db.session.execute('INSERT INTO professor VALUES(:u_id, :name, :phone, :email, :password)',
                    dict(u_id=u_id, name=name, phone=phone, email=email, password=password))
            else:
                db.session.execute('INSERT INTO student VALUES(:u_id, :name, :phone, :email, :password)',
                    dict(u_id=u_id, name=name, phone=phone, email=email, password=password))
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

class Professor(db.Model):
    __tablename__ = 'professor'
    u_id = db.Column('u_id', db.Integer(), db.ForeignKey('Users.u_id'), primary_key=True)
    name = db.Column('name', db.String(256))
    phone = db.Column('phone', db.Integer())
    email = db.Column('email', db.String(256))
    password = db.Column('password', db.String(256))

class Student(db.Model):
    __tablename__ = 'student'
    u_id = db.Column('u_id', db.Integer(), db.ForeignKey('Users.u_id'), primary_key=True)
    name = db.Column('name', db.String(256))
    phone = db.Column('phone', db.Integer())
    email = db.Column('email', db.String(256))
    password = db.Column('password', db.String(256))
    first_major = db.Column('first_major', db.String(256))
    second_major = db.Column('second_major', db.String(256))
    grad_year = db.Column('grad_year', db.Integer())  

class Groups(db.Model):
    __tablename__ = 'groups'
    group_name = db.Column('group_name', db.String(256))
    g_id = db.Column('g_id', db.Integer(), primary_key=True)
    @staticmethod
    def addNew(group_name, section_id, assignment_id, currentuser):
        try:
            g_id = db.session.query(Groups).count()+1
            section_id = int(section_id)
            db.session.execute('INSERT INTO groups VALUES(:group_name, :g_id)',
                               dict(group_name=group_name, g_id=g_id))
            if assignment_id == "none":
                db.session.execute('INSERT INTO studygroup VALUES(:g_id, :name)',
                               dict(g_id=g_id, name=group_name))
                db.session.execute('INSERT INTO studyingfor VALUES(:g_id, :section_id)',
                               dict(g_id=g_id, section_id=section_id))
            else:
                db.session.execute('INSERT INTO projectgroup VALUES(:g_id, :name)',
                                   dict(g_id=g_id, name=group_name))
                db.session.execute('INSERT INTO workingon VALUES(:g_id, :assignment_id)',
                                   dict(g_id=g_id, assignment_id=int(assignment_id)))
            db.session.execute('INSERT INTO memberof VALUES(:u_id, :g_id, :is_leader)',
                dict(u_id=currentuser.u_id, g_id=g_id, is_leader='yes'))
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

class MemberOf(db.Model):
    __tablename__ = 'memberof'
    u_id = db.Column('u_id', db.Integer(), db.ForeignKey('users.u_id'), primary_key=True)
    g_id = db.Column('g_id', db.Integer(), db.ForeignKey('groups.g_id'), primary_key=True)
    is_leader = db.Column('is_leader', db.String(3))

class University(db.Model):
    __tablename__ = 'university'
    university_name = db.Column('university_name', db.String(256), primary_key=True)
    university_location = db.Column('university_location', db.String(256), primary_key=True)

class Post(db.Model):
    __tablename__ = 'post'
    post_id = db.Column('post_id', db.Integer(), primary_key=True)
    assignment_id = db.Column('assignment_id', db.Integer(), db.ForeignKey('projectassignment.assignment_id'), primary_key=True) 
    section_id = db.Column('section_id', db.Integer(), db.ForeignKey('section.section_id'), primary_key=True) 
    u_id = db.Column('u_id', db.Integer(), db.ForeignKey('users.u_id'))
    post_type = db.Column('post_type', db.String(100))
    message = db.Column('message', db.String(1000))
    time_posted = db.Column('time_posted', db.String())
    @staticmethod
    def addNew(assignment_id, section_id, u_id, looking_for, message, time_posted):
        try:
            post_id = db.session.query(Post).count()+1
            post_id = int(post_id)
            section_id = int(section_id)
            db.session.execute('INSERT INTO post VALUES(:post_id, :assignment_id, :section_id, :u_id, :post_type, :message, :time_posted)',
                               dict(post_id = post_id, assignment_id=assignment_id, section_id=section_id,u_id=u_id,post_type=looking_for,message=message,time_posted=time_posted))
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e


class ProjectAssignment(db.Model):
    __tablename__ = 'projectassignment'
    assignment_id = db.Column('assignment_id', db.Integer(), primary_key=True)
    max_members = db.Column('max_members', db.Integer())
    date_assigned = db.Column('date_assigned', db.String(20))
    date_due = db.Column('date_due', db.String(20))
    description = db.Column('description', db.String(1000))
    posts = orm.relationship('Post')

class AssignedTo(db.Model):
    __tablename__ = 'assignedto'
    assignment_id = db.Column('assignment_id', db.String(256), db.ForeignKey('projectassignment.assignment_id'), primary_key=True)
    section_id = db.Column('section_id', db.Integer(), db.ForeignKey('section.section_id'), primary_key=True)      

class Course(db.Model):
    __tablename__ = 'course'
    course_code = db.Column('course_code', db.String(256), primary_key=True)
    course_semester = db.Column('course_semester', db.String(10), primary_key=True)
    university_name = db.Column('university_name', db.String(256), db.ForeignKey('university.university_name'), primary_key=True)
    university_location = db.Column('university_location', db.String(256), db.ForeignKey('university.university_location'), primary_key=True)
    course_name = db.Column('course_name', db.String(256))
    course_pre = db.Column('course_pre', db.String(256))

class Section(db.Model):
    __tablename__ = 'section'
    section_id = db.Column('section_id', db.Integer(), primary_key=True)
    section_number = db.Column('section_number', db.Integer())
    course_code = db.Column('course_code', db.String(256), db.ForeignKey('course.course_code'), primary_key=True)
    course_semester = db.Column('course_semester', db.String(256), db.ForeignKey('course.course_semester'), primary_key=True)
    university_name = db.Column('university_name', db.String(256), db.ForeignKey('university.university_name'), primary_key=True)
    university_location = db.Column('university_location', db.String(256), db.ForeignKey('university.university_location'), primary_key=True)

class RegisteredWith(db.Model):
    __tablename__ = 'registeredwith'
    u_id = db.Column('u_id', db.Integer(), db.ForeignKey('users.u_id'), primary_key=True)
    section_id = db.Column('section_id', db.Integer(), db.ForeignKey('section.section_id'), primary_key=True)
    @staticmethod
    def addNew(u_id, section_id):
        try:
            db.session.execute('INSERT INTO registeredwith VALUES(:u_id, :section_id)',
                               dict(u_id=u_id, section_id=section_id))
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

class Add(db.Model):
    __tablename__ = 'join'
    j_id = db.Column('j_id', db.Integer(), primary_key=True)
    g_id = db.Column('g_id', db.Integer(), db.ForeignKey('groups.g_id'))
    message = db.Column('message', db.String(1000))
    approved = db.Column('approved', db.String(1))
    sent_to = db.Column('sent_to', db.Integer(), db.ForeignKey('users.u_id'))
    sent_by = db.Column('sent_by', db.Integer(), db.ForeignKey('users.u_id'))

class SentTo(db.Model):
    __tablename__ = 'sentto'
    j_id = db.Column('j_id', db.Integer(), db.ForeignKey('join.j_id'), primary_key=True)    
    u_id = db.Column('u_id', db.Integer(), db.ForeignKey('Users.u_id'), primary_key=True)  

class SentBy(db.Model):
    __tablename__ = 'sentby'
    j_id = db.Column('j_id', db.Integer(), db.ForeignKey('join.j_id'), primary_key=True)    
    u_id = db.Column('u_id', db.Integer(), db.ForeignKey('Users.u_id'), primary_key=True)     

class ProjectGroup(db.Model):
    __tablename__ = 'projectgroup'
    g_id = db.Column('g_id', db.Integer(), db.ForeignKey('groups.g_id'), primary_key=True)  
    name = db.Column('name', db.String(256))

class StudyGroup(db.Model):
    __tablename__ = 'studygroup'
    g_id = db.Column('g_id', db.Integer(), db.ForeignKey('groups.g_id'), primary_key=True)  
    name = db.Column('name', db.String(256))

class WorkingOn(db.Model):
    __tablename__ = 'workingon'
    g_id = db.Column('g_id', db.Integer(), db.ForeignKey('groups.g_id'), primary_key=True)
    assignment_id = db.Column('assignment_id', db.Integer(), db.ForeignKey('projectassignment.assignment_id'), primary_key=True)         

class StudyingFor(db.Model):
    __tablename__ = 'studyingfor'
    g_id = db.Column('g_id', db.Integer(), db.ForeignKey('groups.g_id'), primary_key=True)
    section_id = db.Column('section_id', db.Integer(), db.ForeignKey('section.section_id'), primary_key=True)

class GroupResponse(db.Model):
    __tablename__ = 'groupresponse'
    post_id = db.Column('post_id', db.Integer(), db.ForeignKey('post.post_id'), primary_key=True)
    g_id = db.Column('g_id', db.Integer(), db.ForeignKey('groups.g_id'), primary_key=True)
    section_id = db.Column('section_id', db.Integer(), db.ForeignKey('section.section_id'), primary_key=True)
    time_posted = db.Column('time_posted', db.String(100))
    message = db.Column('message', db.String(1000))
    approved = db.Column('approved', db.Boolean())
    @staticmethod
    def addNew(post_id, g_id, section_id, message):
        try:
            time = str(datetime.datetime.now())
            db.session.execute('INSERT INTO groupresponse VALUES(:post_id, :g_id, :section_id, :time_posted, :message, :approved)',
                               dict(post_id=post_id, g_id=g_id, section_id=section_id, time_posted=time, message=message, approved=False))
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

class UserResponse(db.Model):
    __tablename__ = 'userresponse'
    post_id = db.Column('post_id', db.Integer(), db.ForeignKey('post.post_id'), primary_key=True)
    u_id = db.Column('u_id', db.Integer(), db.ForeignKey('users.u_id'), primary_key=True)
    section_id = db.Column('section_id', db.Integer(), db.ForeignKey('section.section_id'), primary_key=True)
    time_posted = db.Column('time_posted', db.String())
    message = db.Column('message', db.String(1000))
    approved = db.Column('approved', db.Boolean())
    @staticmethod
    def addNew(post_id, u_id, section_id, message):
        try:
            time = str(datetime.datetime.now())
            db.session.execute('INSERT INTO userresponse VALUES(:post_id, :u_id, :section_id, :time_posted, :m\
essage, :approved)',
                               dict(post_id=post_id, u_id=u_id, section_id=section_id, time_posted=time, message=message, approved=False))
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
