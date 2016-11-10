\COPY Bar(name, address) FROM 'data/Bar.dat' WITH DELIMITER ',' NULL '' CSV
\COPY Beer(name, brewer) FROM 'data/Beer.dat' WITH DELIMITER ',' NULL '' CSV
\COPY Drinker(name, address) FROM 'data/Drinker.dat' WITH DELIMITER ',' NULL '' CSV
\COPY Frequents(drinker, bar, times_a_week) FROM 'data/Frequents.dat' WITH DELIMITER ',' NULL '' CSV
\COPY Serves(bar, beer, price) FROM 'data/Serves.dat' WITH DELIMITER ',' NULL '' CSV
\COPY Likes(drinker, beer) FROM 'data/Likes.dat' WITH DELIMITER ',' NULL '' CSV

\COPY SchoolUser(u_id, name, phone, email) FROM 'data/SchoolUser.dat' WITH DELIMITER ',' NULL '' CSV
\COPY Professor(u_id, name, phone, email) FROM 'data/Professor.dat' WITH DELIMITER ',' NULL '' CSV
\COPY Student(u_id, name, phone, email, first_major, second_major, grad_year) FROM 'data/Student.dat' WITH DELIMITER ',' NULL '' CSV
\COPY SchoolGroup(g_id, group_name) FROM 'data/SchoolGroup.dat' WITH DELIMITER ',' NULL '' CSV
\COPY MemberOf(u_id, g_id, is_leader) FROM 'data/MemberOf.dat' WITH DELIMITER ',' NULL '' CSV
\COPY University(university_name, university_location) FROM 'data/University.dat' WITH DELIMITER ',' NULL '' CSV
\COPY Class(class_code, class_semester, university_name, university_location) FROM 'data/Class.dat' WITH DELIMITER ',' NULL '' CSV
\COPY Section(section_number, class_code, class_semester, university_name, university_location) FROM 'data/Section.dat' WITH DELIMITER ',' NULL '' CSV
\COPY RegisteredWith(u_id, section_number, class_code, class_semester, university_name, university_location) FROM 'data/RegisteredWith.dat' WITH DELIMITER ',' NULL '' CSV
\COPY Add(j_id, message, approved) FROM 'data/Add.dat' WITH DELIMITER ',' NULL '' CSV
\COPY SentTo(j_id, u_id) FROM 'data/SentTo.dat' WITH DELIMITER ',' NULL '' CSV
\COPY SentBy(j_id, u_id) FROM 'data/SentBy.dat' WITH DELIMITER ',' NULL '' CSV
\COPY ProjectAssignment(assignment_id, max_members, date_assigned, date_due, description) FROM 'data/ProjectAssignment.dat' WITH DELIMITER ',' NULL '' CSV
\COPY AssignedTo(assignment_id, section_number, class_code, class_semester, university_name, university_location) FROM 'data/AssignedTo.dat' WITH DELIMITER ',' NULL '' CSV
\COPY Post(assignment_id, time_posted, message) FROM 'data/Post.dat' WITH DELIMITER ',' NULL '' CSV
\COPY NeedTeamPost(assignment_id, u_id) FROM 'data/NeedTeamPost.dat' WITH DELIMITER ',' NULL '' CSV
\COPY NeedMemberPost(assignment_id, g_id) FROM 'data/NeedMemberPost.dat' WITH DELIMITER ',' NULL '' CSV
\COPY ProjectGroup(g_id, name) FROM 'data/ProjectGroup.dat' WITH DELIMITER ',' NULL '' CSV
\COPY StudyGroup(g_id, name) FROM 'data/StudyGroup.dat' WITH DELIMITER ',' NULL '' CSV
\COPY WorkingOn(assignment_id, g_id) FROM 'data/WorkingOn.dat' WITH DELIMITER ',' NULL '' CSV
\COPY StudyingFor(g_id, class_code, class_semester, university_name, university_location) FROM 'data/StudyingFor.dat' WITH DELIMITER ',' NULL '' CSV
