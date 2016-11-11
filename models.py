from sqlalchemy import sql, orm
from app import db

class SchoolUser(db.Model):
    __tablename__ = 'schooluser'
    u_id = db.Column('u_id', db.Integer(), primary_key=True)
    name = db.Column('name', db.String(256))
    phone = db.Column('phone', db.String(10))
    email = db.Column('email', db.String(256))
    @staticmethod
    def addNew(name, phone, email, user_type):
        try:
            u_id = db.session.query(SchoolUser).count()+1
            db.session.execute('INSERT INTO schooluser VALUES(:u_id, :name, :phone, :email)',
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
    u_id = db.Column('u_id', db.Integer(), db.ForeignKey('schooluser.u_id'), primary_key=True)
    name = db.Column('name', db.String(256))
    phone = db.Column('phone', db.Integer())
    email = db.Column('email', db.String(256))   

class Student(db.Model):
    __tablename__ = 'student'
    u_id = db.Column('u_id', db.Integer(), db.ForeignKey('schooluser.u_id'), primary_key=True)
    name = db.Column('name', db.String(256))
    phone = db.Column('phone', db.Integer())
    email = db.Column('email', db.String(256))  
    first_major = db.Column('first_major', db.String(256))
    second_major = db.Column('second_major', db.String(256))
    grad_year = db.Column('grad_year', db.Integer())  

class SchoolGroup(db.Model):
    __tablename__ = 'schoolgroup'
    g_id = db.Column('g_id', db.Integer(), primary_key=True)
    group_name = db.Column('group_name', db.String(256))
    @staticmethod
    def addNew(group_name, course, currentuser):
        try:
            g_id = db.session.query(SchoolGroup).count()+1
            db.session.execute('INSERT INTO groups VALUES(:g_id, :group_name)',
                               dict(g_id=g_id, group_name=group_name))
            db.session.execute('INSERT INTO studygroup VALUES(:g_id, :name)',
                               dict(g_id=g_id, name=group_name))
            db.session.execute('INSERT INTO studyingfor VALUES(:g_id, :course_code, :course_semester, :university_name, :university_location)',
                dict(g_id=g_id, course_code=course.course_code, course_semester=course.course_semester, university_name=course.university_name, university_location=course.university_location))
            db.session.execute('INSERT INTO memberof VALUES(:u_id, :g_id, :is_leader)',
                dict(u_id=currentuser.u_id, g_id=g_id, is_leader='y'))
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

class MemberOf(db.Model):
    __tablename__ = 'memberof'
    u_id = db.Column('u_id', db.Integer(), db.ForeignKey('schooluser.u_id'), primary_key=True)
    g_id = db.Column('g_id', db.Integer(), db.ForeignKey('schoolgroup.g_id'), primary_key=True)
    is_leader = db.Column('is_leader', db.String(3))

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
    u_id = db.Column('u_id', db.Integer(), db.ForeignKey('schooluser.u_id'), primary_key=True)    
    section_number = db.Column('section_number', db.Integer(), db.ForeignKey('section.section_number'), primary_key=True)
    course_code = db.Column('course_code', db.String(256), db.ForeignKey('course.course_code'), primary_key=True)
    course_semester = db.Column('course_semester', db.String(256), db.ForeignKey('course.course_semester'), primary_key=True)
    university_name = db.Column('university_name', db.String(256), db.ForeignKey('university.university_name'), primary_key=True)
    university_location = db.Column('university_location', db.String(256), db.ForeignKey('university.university_location'), primary_key=True)

class Add(db.Model):
    __tablename__ = 'join'
    j_id = db.Column('j_id', db.Integer(), primary_key=True)
    message = db.Column('message', db.String(1000))
    approved = db.Column('approved', db.String(1))

class SentTo(db.Model):
    __tablename__ = 'sentto'
    j_id = db.Column('j_id', db.Integer(), db.ForeignKey('join.j_id'), primary_key=True)    
    u_id = db.Column('u_id', db.Integer(), db.ForeignKey('schooluser.u_id'), primary_key=True)  

class SentBy(db.Model):
    __tablename__ = 'sentby'
    j_id = db.Column('j_id', db.Integer(), db.ForeignKey('join.j_id'), primary_key=True)    
    u_id = db.Column('u_id', db.Integer(), db.ForeignKey('schooluser.u_id'), primary_key=True)    
    
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
    time_posted = db.Column('time_posted', db.Integer())
    message = db.Column('message', db.String(1000))

class NeedTeamPost(db.Model):
    __tablename__ = 'needteampost'
    assignment_id = db.Column('assignment_id', db.Integer(), db.ForeignKey('projectassignment.assignment_id'), primary_key=True)   
    u_id = db.Column('u_id', db.Integer(), db.ForeignKey('schooluser.u_id'), primary_key=True)  

class NeedMemberPost(db.Model):
    __tablename__ = 'needmemberpost'
    assignment_id = db.Column('assignment_id', db.Integer(), db.ForeignKey('projectassignment.assignment_id'), primary_key=True)   
    g_id = db.Column('g_id', db.Integer(), db.ForeignKey('schoolgroup.g_id'), primary_key=True)

class ProjectGroup(db.Model):
    __tablename__ = 'projectgroup'
    g_id = db.Column('g_id', db.Integer(), db.ForeignKey('schoolgroup.g_id'), primary_key=True)  
    name = db.Column('name', db.String(256))

class StudyGroup(db.Model):
    __tablename__ = 'studygroup'
    g_id = db.Column('g_id', db.Integer(), db.ForeignKey('schoolgroup.g_id'), primary_key=True)  
    name = db.Column('name', db.String(256))

class WorkingOn(db.Model):
    __tablename__ = 'workingon'
    assignment_id = db.Column('assignment_id', db.Integer(), db.ForeignKey('projectassignment.assignment_id'), primary_key=True)
    g_id = db.Column('g_id', db.Integer(), db.ForeignKey('schoolgroup.g_id'), primary_key=True)         

class StudyingFor(db.Model):
    __tablename__ = 'studyingfor'
    g_id = db.Column('g_id', db.Integer(), db.ForeignKey('schoolgroup.g_id'), primary_key=True)
    course_code = db.Column('course_code', db.String(256), db.ForeignKey('course.course_code'), primary_key=True)
    course_semester = db.Column('course_semester', db.String(256), db.ForeignKey('course.course_semester'), primary_key=True) 
    university_name = db.Column('university_name', db.String(256), db.ForeignKey('course.university_name'), primary_key=True)
    university_location = db.Column('university_location', db.String(256), db.ForeignKey('course.university_location'), primary_key=True)

class Drinker(db.Model):
    __tablename__ = 'drinker'
    name = db.Column('name', db.String(20), primary_key=True)
    address = db.Column('address', db.String(20))
    likes = orm.relationship('Likes')
    frequents = orm.relationship('Frequents')
    @staticmethod
    def addNew(name, address, beers_liked, bars_frequented):
        try:
            db.session.execute('INSERT INTO drinker VALUES(:name, :address)',
                               dict(name=name, address=address))
            for beer in beers_liked:
                db.session.execute('INSERT INTO likes VALUES(:drinker, :beer)',
                                   dict(drinker=name, beer=beer))
            for bar, times_a_week in bars_frequented:
                db.session.execute('INSERT INTO frequents'
                                   ' VALUES(:drinker, :bar, :times_a_week)',
                                   dict(drinker=name, bar=bar,
                                        times_a_week=times_a_week))
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def edit(old_name, name, address, beers_liked, bars_frequented):
        try:
            db.session.execute('DELETE FROM likes WHERE drinker = :name',
                               dict(name=old_name))
            db.session.execute('DELETE FROM frequents WHERE drinker = :name',
                               dict(name=old_name))
            db.session.execute('UPDATE drinker SET name = :name, address = :address'
                               ' WHERE name = :old_name',
                               dict(old_name=old_name, name=name, address=address))
            for beer in beers_liked:
                db.session.execute('INSERT INTO likes VALUES(:drinker, :beer)',
                                   dict(drinker=name, beer=beer))
            for bar, times_a_week in bars_frequented:
                db.session.execute('INSERT INTO frequents'
                                   ' VALUES(:drinker, :bar, :times_a_week)',
                                   dict(drinker=name, bar=bar,
                                        times_a_week=times_a_week))
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

class Beer(db.Model):
    __tablename__ = 'beer'
    name = db.Column('name', db.String(20), primary_key=True)
    brewer = db.Column('brewer', db.String(20))

class Bar(db.Model):
    __tablename__ = 'bar'
    name = db.Column('name', db.String(20), primary_key=True)
    address = db.Column('address', db.String(20))
    serves = orm.relationship('Serves')

class Likes(db.Model):
    __tablename__ = 'likes'
    drinker = db.Column('drinker', db.String(20),
                        db.ForeignKey('drinker.name'),
                        primary_key=True)
    beer = db.Column('beer', db.String(20),
                     db.ForeignKey('beer.name'),
                     primary_key=True)

class Serves(db.Model):
    __tablename__ = 'serves'
    bar = db.Column('bar', db.String(20),
                    db.ForeignKey('bar.name'),
                    primary_key=True)
    beer = db.Column('beer', db.String(20),
                     db.ForeignKey('beer.name'),
                     primary_key=True)
    price = db.Column('price', db.Float())

class Frequents(db.Model):
    __tablename__ = 'frequents'
    drinker = db.Column('drinker', db.String(20),
                        db.ForeignKey('drinker.name'),
                        primary_key=True)
    bar = db.Column('bar', db.String(20),
                    db.ForeignKey('bar.name'),
                    primary_key=True)
    times_a_week = db.Column('times_a_week', db.Integer())
