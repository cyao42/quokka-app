from sqlalchemy import sql, orm
from app import db

class Users(db.Model):
    __tablename__ = 'users'
    u_id = db.Column('u_id', db.Integer(), primary_key=True)
    name = db.Column('name', db.String(256))
    phone = db.Column('phone', db.String(15))
    email = db.Column('email', db.String(256))
    @staticmethod
    def addNew(name, phone, email, user_type):
        try:
            u_id = db.session.query(Users).count()+1
            db.session.execute('INSERT INTO Users VALUES(:u_id, :name, :phone, :email)',
                               dict(u_id=u_id, name=name, phone=phone, email=email))
            if user_type == 'pro':
                db.session.execute('INSERT INTO professor VALUES(:u_id, :name, :phone, :email)',
                    dict(u_id=u_id, name=name, phone=phone, email=email))  
            else:
                db.session.execute('INSERT INTO student VALUES(:u_id, :name, :phone, :email)',
                    dict(u_id=u_id, name=name, phone=phone, email=email))
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

class Student(db.Model):
    __tablename__ = 'student'
    u_id = db.Column('u_id', db.Integer(), db.ForeignKey('Users.u_id'), primary_key=True)
    name = db.Column('name', db.String(256))
    phone = db.Column('phone', db.Integer())
    email = db.Column('email', db.String(256))  
    first_major = db.Column('first_major', db.String(256))
    second_major = db.Column('second_major', db.String(256))
    grad_year = db.Column('grad_year', db.Integer())  

class Groups(db.Model):
    __tablename__ = 'groups'
    group_name = db.Column('group_name', db.String(256))
    g_id = db.Column('g_id', db.Integer(), primary_key=True)

class MemberOf(db.Model):
    __tablename__ = 'memberof'
    u_id = db.Column('u_id', db.Integer(), db.ForeignKey('Users.u_id'), primary_key=True)
    g_id = db.Column('g_id', db.Integer(), db.ForeignKey('Groups.g_id'), primary_key=True)
    is_leader = db.Column('is_leader', db.Boolean())

class University(db.Model):
    __tablename__ = 'university'
    university_name = db.Column('university_name', db.String(256), primary_key=True)
    university_location = db.Column('university_location', db.String(256), primary_key=True)

class Course(db.Model):
    __tablename__ = 'course'
    course_code = db.Column('course_code', db.String(256), primary_key=True)
    course_semester = db.Column('course_semester', db.String(10), primary_key=True)
    university_name = db.Column('university_name', db.String(256), db.ForeignKey('university.university_name'), primary_key=True)
    university_location = db.Column('university_location', db.String(256), db.ForeignKey('university.university_location'), primary_key=True)

class Section(db.Model):
    __tablename__ = 'section'
    section_number = db.Column('section_number', db.Integer(), primary_key=True)
    course_code = db.Column('course_code', db.String(256), db.ForeignKey('course.course_code'), primary_key=True)
    course_semester = db.Column('course_semester', db.String(256), db.ForeignKey('course.course_semester'), primary_key=True)
    university_name = db.Column('university_name', db.String(256), db.ForeignKey('university.university_name'), primary_key=True)
    university_location = db.Column('university_location', db.String(256), db.ForeignKey('university.university_location'), primary_key=True)

class RegisteredWith(db.Model):
    __tablename__ = 'registeredwith'
    u_id = db.Column('u_id', db.Integer(), db.ForeignKey('Users.u_id'), primary_key=True)    
    section_number = db.Column('section_number', db.Integer(), db.ForeignKey('section.section_number'), primary_key=True)
    course_code = db.Column('course_code', db.String(256), db.ForeignKey('course.course_code'), primary_key=True)
    course_semester = db.Column('course_semester', db.String(256), db.ForeignKey('course.course_semester'), primary_key=True)
    university_name = db.Column('university_name', db.String(256), db.ForeignKey('university.university_name'), primary_key=True)
    university_location = db.Column('university_location', db.String(256), db.ForeignKey('university.university_location'), primary_key=True)

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
    
class ProjectAssignment(db.Model):
    __tablename__ = 'projectassignment'
    assignment_id = db.Column('assignment_id', db.Integer(), primary_key=True)
    max_members = db.Column('max_members', db.Integer())
    date_assigned = db.Column('date_assigned', db.String(20))
    date_due = db.Column('date_due', db.String(20))
    description = db.Column('description', db.String(1000))

class AssignedTo(db.Model):
    __tablename__ = 'assignedto'
    assignment_id = db.Column('assignment_id', db.String(256), db.ForeignKey('projectassignment.assignment_id'), primary_key=True)
    section_number = db.Column('section_number', db.Integer(), db.ForeignKey('section.section_number'), primary_key=True)    
    course_code = db.Column('course_code', db.String(256), db.ForeignKey('course.course_code'), primary_key=True)
    course_semester = db.Column('course_semester', db.String(256), db.ForeignKey('course.course_semester'), primary_key=True)
    university_name = db.Column('university_name', db.String(256), db.ForeignKey('university.university_name'), primary_key=True)
    university_location = db.Column('university_location', db.String(256), db.ForeignKey('university.university_location'), primary_key=True)

class Post(db.Model):
    __tablename__ = 'post'
    assignment_id = db.Column('assignment_id', db.Integer(), db.ForeignKey('projectassignment.assignment_id'), primary_key=True) 
    time_posted = db.Column('time_posted', db.String(), primary_key=True)
    message = db.Column('message', db.String(1000))

class NeedTeamPost(db.Model):
    __tablename__ = 'needteampost'
    assignment_id = db.Column('assignment_id', db.Integer(), db.ForeignKey('projectassignment.assignment_id'), primary_key=True)   
    u_id = db.Column('u_id', db.Integer(), db.ForeignKey('Users.u_id'), primary_key=True)  

class NeedMemberPost(db.Model):
    __tablename__ = 'needmemberpost'
    assignment_id = db.Column('assignment_id', db.Integer(), db.ForeignKey('projectassignment.assignment_id'), primary_key=True)   
    g_id = db.Column('g_id', db.Integer(), db.ForeignKey('Groups.g_id'), primary_key=True)

class ProjectGroup(db.Model):
    __tablename__ = 'projectgroup'
    g_id = db.Column('g_id', db.Integer(), db.ForeignKey('Groups.g_id'), primary_key=True)  
    name = db.Column('name', db.String(256))

class StudyGroup(db.Model):
    __tablename__ = 'studygroup'
    g_id = db.Column('g_id', db.Integer(), db.ForeignKey('Groups.g_id'), primary_key=True)  
    name = db.Column('name', db.String(256))

class WorkingOn(db.Model):
    __tablename__ = 'workingon'
    g_id = db.Column('g_id', db.Integer(), db.ForeignKey('Groups.g_id'), primary_key=True)
    assignment_id = db.Column('assignment_id', db.Integer(), db.ForeignKey('projectassignment.assignment_id'), primary_key=True)         

class StudyingFor(db.Model):
    __tablename__ = 'studyingfor'
    g_id = db.Column('g_id', db.Integer(), db.ForeignKey('Groups.g_id'), primary_key=True)
    section_number = db.Column('section_number', db.Integer(), db.ForeignKey('Section.section_number'), primary_key=True)
    course_code = db.Column('course_code', db.String(256), db.ForeignKey('course.course_code'), primary_key=True)
    course_semester = db.Column('course_semester', db.String(256), db.ForeignKey('course.course_semester'), primary_key=True) 
    university_name = db.Column('university_name', db.String(256), db.ForeignKey('course.university_name'), primary_key=True)
    university_location = db.Column('university_location', db.String(256), db.ForeignKey('course.university_location'), primary_key=True)
