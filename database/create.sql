CREATE TABLE SchoolUser
(u_id INTEGER NOT NULL PRIMARY KEY,
 name VARCHAR(256) NOT NULL,
 phone VARCHAR(10) NOT NULL,
 email VARCHAR(256) NOT NULL
);

CREATE TABLE Professor
(u_id INTEGER NOT NULL UNIQUE PRIMARY KEY REFERENCES SchoolUser(u_id),
 name VARCHAR(256) NOT NULL,
 phone VARCHAR(10) NOT NULL,
 email VARCHAR(256) NOT NULL
);

CREATE TABLE Student
(u_id INTEGER NOT NULL UNIQUE PRIMARY KEY REFERENCES SchoolUser(u_id),
 name VARCHAR(256) NOT NULL,
 phone VARCHAR(10) NOT NULL,
 email VARCHAR(256) NOT NULL,
 first_major VARCHAR(256), 
 second_major VARCHAR(256),
 grad_year INTEGER NOT CHECK (grad_year > 0)
);

CREATE TABLE SchoolGroup
(g_id INTEGER NOT NULL UNIQUE PRIMARY KEY,
 group_name VARCHAR(256) NOT NULL
);

CREATE TABLE MemberOf
(u_id INTEGER NOT NULL UNIQUE REFERENCES SchoolUser(u_id),
 g_id INTEGER NOT NULL REFERENCES SchoolGroup(g_id),
 is_leader CHAR(1) NOT NULL CHECK (is_leader IN ('t', 'f')),
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
(u_id INTEGER NOT NULL UNIQUE REFERENCES SchoolUser(u_id),
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
 message VARCHAR(1000),
 approved CHAR(1) NOT NULL CHECK (approved IN ('y', 'n'))
);

CREATE TABLE SentTo 
(j_id INTEGER NOT NULL REFERENCES Add(j_id),
 u_id INTEGER NOT NULL REFERENCES SchoolUser(u_id),
 PRIMARY KEY (j_id, u_id)
);

CREATE TABLE SentBY 
(j_id INTEGER NOT NULL REFERENCES Add(j_id),
 u_id INTEGER NOT NULL REFERENCES SchoolUser(u_id),
 PRIMARY KEY (j_id, u_id)
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
(assignment_id INTEGER NOT NULL PRIMARY KEY REFERENCES ProjectAssignment(assignment_id),
 time_posted INTEGER NOT NULL,
 message VARCHAR(1000)
);

CREATE TABLE NeedTeamPost
(assignment_id INTEGER NOT NULL REFERENCES ProjectAssignment(assignment_id),
 u_id INTEGER NOT NULL REFERENCES SchoolUser(u_id),
 PRIMARY KEY (assignment_id, u_id)
);

CREATE TABLE NeedMemberPost
(assignment_id INTEGER NOT NULL REFERENCES ProjectAssignment(assignment_id),
 g_id INTEGER NOT NULL REFERENCES SchoolGroup(g_id),
 PRIMARY KEY (assignment_id, g_id)
);

CREATE TABLE ProjectGroup
(g_id INTEGER NOT NULL PRIMARY KEY REFERENCES SchoolGroup(g_id),
 name VARCHAR(256) NOT NULL
);

CREATE TABLE StudyGroup
(g_id INTEGER NOT NULL PRIMARY KEY REFERENCES SchoolGroup(g_id),
 name VARCHAR(256) NOT NULL
);

CREATE TABLE WorkingOn
(assignment_id INTEGER NOT NULL REFERENCES ProjectAssignment(assignment_id),
 g_id INTEGER NOT NULL REFERENCES ProjectGroup(g_id),
 PRIMARY KEY (assignment_id, g_id)
);

CREATE TABLE StudyingFor 
(g_id INTEGER NOT NULL REFERENCES SchoolGroup(g_id),
 class_code VARCHAR(256) NOT NULL,
 class_semester VARCHAR(256) NOT NULL,
 university_name VARCHAR(256) NOT NULL,
 university_location VARCHAR(256) NOT NULL,
 PRIMARY KEY (g_id,class_code,class_semester,university_name,university_location),
 FOREIGN KEY (class_code, class_semester, university_name, university_location)
 REFERENCES Class(class_code, class_semester, university_name, university_location)
);

CREATE TABLE Bar(name VARCHAR(20) NOT NULL PRIMARY KEY,
                 address VARCHAR(20));
CREATE TABLE Beer(name VARCHAR(20) NOT NULL PRIMARY KEY,
                  brewer VARCHAR(20));
CREATE TABLE Drinker(name VARCHAR(20) NOT NULL PRIMARY KEY,
                     address VARCHAR(20));
CREATE TABLE Frequents(drinker VARCHAR(20) NOT NULL REFERENCES Drinker(name),
                       bar VARCHAR(20) NOT NULL REFERENCES Bar(name),
                       times_a_week SMALLINT CHECK(times_a_week > 0),
                       PRIMARY KEY(drinker, bar));
CREATE TABLE Serves(bar VARCHAR(20) NOT NULL REFERENCES Bar(name),
                    beer VARCHAR(20) NOT NULL REFERENCES Beer(name),
                    price DECIMAL(5,2) CHECK(price > 0),
                    PRIMARY KEY(bar, beer));
CREATE TABLE Likes(drinker VARCHAR(20) NOT NULL REFERENCES Drinker(name),
                   beer VARCHAR(20) NOT NULL REFERENCES Beer(name),
                   PRIMARY KEY(drinker, beer));
