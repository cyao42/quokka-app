CREATE TABLE Users
(u_id INTEGER NOT NULL PRIMARY KEY,
 name VARCHAR(256) NOT NULL,
 phone VARCHAR(15) NOT NULL,
 email VARCHAR(256) NOT NULL
);

CREATE TABLE Professor
(u_id INTEGER NOT NULL UNIQUE PRIMARY KEY REFERENCES Users(u_id),
 name VARCHAR(256) NOT NULL,
 phone VARCHAR(15) NOT NULL,
 email VARCHAR(256) NOT NULL
);

CREATE TABLE Student
(u_id INTEGER NOT NULL UNIQUE PRIMARY KEY REFERENCES Users(u_id),
 name VARCHAR(256) NOT NULL,
 phone VARCHAR(15) NOT NULL,
 email VARCHAR(256) NOT NULL,
 first_major VARCHAR(256), 
 second_major VARCHAR(256),
 grad_year INTEGER CHECK (grad_year > 0)
);

CREATE TABLE Groups
(group_name VARCHAR(256) NOT NULL,
g_id INTEGER NOT NULL UNIQUE PRIMARY KEY
);

CREATE TABLE MemberOf
(u_id INTEGER NOT NULL UNIQUE REFERENCES Users(u_id),
 g_id INTEGER NOT NULL REFERENCES Groups(g_id),
 is_leader CHAR(3) NOT NULL CHECK (is_leader IN ('yes', 'no')),
 PRIMARY KEY (u_id,g_id)
);

CREATE TABLE University
(university_name VARCHAR(265) NOT NULL,
 university_location VARCHAR(265) NOT NULL,
 PRIMARY KEY (university_name, university_location)
);

CREATE TABLE Class
(class_code VARCHAR(256) NOT NULL,
 class_semester VARCHAR(256) NOT NULL,
 university_name VARCHAR(256) NOT NULL,
 university_location VARCHAR(256) NOT NULL,
 PRIMARY KEY (class_code,class_semester,university_name,university_location),
FOREIGN KEY (university_name, university_location) REFERENCES University (university_name, university_location)
);

CREATE TABLE Section
(section_number INTEGER NOT NULL,
 class_code     VARCHAR(256) NOT NULL,
 class_semester VARCHAR(256) NOT NULL,
 university_name VARCHAR(256) NOT NULL,
 university_location VARCHAR(256) NOT NULL,
 PRIMARY KEY (section_number,class_code,class_semester,university_name,university_location),
FOREIGN KEY (class_code, class_semester, university_name, university_location) REFERENCES Class (class_code, class_semester, university_name, university_location)
);

CREATE TABLE RegisteredWith
(u_id INTEGER NOT NULL UNIQUE REFERENCES Users(u_id),
 section_number INTEGER NOT NULL,
 class_code VARCHAR(256) NOT NULL,
 class_semester VARCHAR(265) NOT NULL,
 university_name VARCHAR(265) NOT NULL,
 university_location VARCHAR(265) NOT NULL,
 PRIMARY KEY (u_id,section_number,class_code,class_semester,university_name,university_location),
FOREIGN KEY (section_number, class_code, class_semester, university_name, university_location)
REFERENCES Section (section_number, class_code, class_semester, university_name, university_location)
);

CREATE TABLE Add 
(j_id INTEGER NOT NULL PRIMARY KEY,
 g_id INTEGER REFERENCES Groups(g_id),
 message VARCHAR(1000),
 approved CHAR(3) NOT NULL CHECK (approved IN ('yes', 'no')),
 sent_to INTEGER REFERENCES Users(u_id),
 sent_by INTEGER REFERENCES Users(u_id)
);

CREATE TABLE ProjectAssignment
(assignment_id INTEGER NOT NULL PRIMARY KEY,
 max_members INTEGER,
 date_assigned VARCHAR(20),
 date_due VARCHAR(20),
 description VARCHAR(1000)
);

CREATE TABLE AssignedTo 
(assignment_id INTEGER NOT NULL REFERENCES ProjectAssignment(assignment_id),
 section_number INTEGER NOT NULL,
 class_code VARCHAR(256) NOT NULL,
 class_semester VARCHAR(256) NOT NULL,
 university_name VARCHAR(256) NOT NULL,
 university_location VARCHAR(256) NOT NULL,
 PRIMARY KEY (assignment_id,section_number,class_code,class_semester,university_name,university_location),
FOREIGN KEY (section_number, class_code, class_semester, university_name, university_location)
REFERENCES Section (section_number, class_code, class_semester, university_name, university_location)
);

CREATE TABLE Post
(assignment_id INTEGER NOT NULL REFERENCES ProjectAssignment(assignment_id),
 time_posted VARCHAR(100) NOT NULL,
 message VARCHAR(1000),
 PRIMARY KEY (assignment_id, time_posted)
);

CREATE TABLE NeedTeamPost
(assignment_id INTEGER NOT NULL REFERENCES ProjectAssignment(assignment_id),
 u_id INTEGER NOT NULL REFERENCES Users(u_id),
 PRIMARY KEY (assignment_id, u_id)
);

CREATE TABLE NeedMemberPost
(assignment_id INTEGER NOT NULL REFERENCES ProjectAssignment(assignment_id),
 g_id INTEGER NOT NULL REFERENCES Groups(g_id),
 PRIMARY KEY (assignment_id, g_id)
);

CREATE TABLE ProjectGroup
(g_id INTEGER NOT NULL PRIMARY KEY REFERENCES Groups(g_id),
 name VARCHAR(256) NOT NULL
);

CREATE TABLE StudyGroup
(g_id INTEGER NOT NULL PRIMARY KEY REFERENCES Groups(g_id),
 name VARCHAR(256) NOT NULL
);

CREATE TABLE WorkingOn
(g_id INTEGER NOT NULL REFERENCES ProjectGroup(g_id),
 assignment_id INTEGER NOT NULL REFERENCES ProjectAssignment(assignment_id),
 PRIMARY KEY (g_id, assignment_id)
);

CREATE TABLE StudyingFor 
(g_id INTEGER NOT NULL REFERENCES Groups(g_id),
 section_number INTEGER,
 class_code VARCHAR(256) NOT NULL,
 class_semester VARCHAR(256) NOT NULL,
 university_name VARCHAR(256) NOT NULL,
 university_location VARCHAR(256) NOT NULL,
 PRIMARY KEY (g_id,section_number,class_code,class_semester,university_name,university_location),
 FOREIGN KEY (section_number,class_code, class_semester, university_name, university_location)
 REFERENCES Section(section_number,class_code, class_semester, university_name, university_location)
);

--List the names and groups of all leaders.--

SELECT Users.name, group_name FROM Users, Groups, MemberOf
WHERE MemberOf.u_id = Users.u_id AND MemberOf.g_id = Groups.g_id AND MemberOf.is_leader = 'yes';

--List names of all users who have posted that they need a team, but are now part of a group.--

SELECT Users.name FROM Users NATURAL JOIN NeedTeamPost NATURAL JOIN MemberOf NATURAL JOIN Groups;

--List the names of all users who are not part of a group.--

SELECT Users.name FROM Users EXCEPT (SELECT Users.name FROM Users NATURAL JOIN MemberOf NATURAL JOIN Groups);

--List the project descriptions of projects that have been assigned for CS316.

SELECT ProjectAssignment.description FROM ProjectAssignment NATURAL JOIN AssignedTo WHERE AssignedTo.class_code = '431';
