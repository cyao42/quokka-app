# quokka-app
A data-oriented app for students to form study groups and find groups for class projects.

README!

Small Sample Database SetUp:
Start up the vm environment. We use the vagrant up command.
Navigate to the directory containing the test-sample.sql file. 
Create the Quokka database by typing in...
	'dropdb quokka; createdb quokka; psql quokka -af test-sample.sql'
Create a sample output file by typing in...
	'dropdb quokka; createdb quokka; psql quokka -af test-sample.sql &> test-sample-out.txt'
A file with the query outputs called 'test-sample-out.txt' should now be created. 

The ‘quokka_setup.sql’ file contains all the create table statements needed for creating
the database as well as insert statements to create a small sample dataset. Running the command…'dropdb quokka; createdb quokka; psql quokka -af quokka_setup.sql' will setup the initial database without the query print outs form the test-sample files.

Large Production Database SetUp:
Our production database is setup and ran much like the example beers database. 
We navigate to the one level above the quokka-app folder and run the following command:
	~../quokka-app/database/setup.sh
The set up executable uses the load.sql and create.sql files to create the database schema and then load the large production data files, which are all .dat files located in a data folder. 

* Note: There is a small caveat. This process requires a small config change depending on if the developer is running/setting up the database on google cloud or on vagrant. We are working to make this process more general. 

The production data files were all custom generated using generatedata.com for some initial random values. The data was produced to fit the schema, and thus no code was required to extract data into a usable form. The data was made to have many dependencies across tables and thus give interesting results when running our sequel commands. These dependencies were complex to set up the initial data and required human effort rather than code. SQL code was updated after the data was generated to fix some inconsistencies. In addition, the TextStripperForData.java file was used to properly convert and print .csv file text to a .dat usable format.


###### How to Set Up Our Project

From VM/Google Cloud,


In quokka-app,
Setup the database: dabatase/setup.sh


Keep one vm terminal window open
In the other,  run: python app.py 


In your browser (in VM), go to localhost:5000 if you are in VM or go to your external IP address:5000 if on google cloud. 


In the vm terminal where you’re free to type, vim config.py and make sure in the SQLALCHEMY_DATABASE_URI that between that you either replace vagrant with your cloud username or keep vagrant there (if you’re using vagrant). 


Once the Quokka home page loads, you can register as a user. You can register as either a student or a professor. If you’re a professor, your profile will look different and you’ll be able to add classes and assignments. If you’re a student, your profile will allow you to enroll into classes and add groups. 


Once you’re a user, you can click on the Quokka (the cute animal) anytime to go to your profile. 


You’re not in any classes yet. Go to add class and enter in section code 15 to start populating your profile.


You can also add a group for whichever class. It should show up. When you click on a group, it will show you the members of that group.


You’ll be added into a class! You can go to “See Posts and Find Mates” button to go to the assignments for that class. Click the assignments you would like to see the posts for, then go to Get Feed. 


Now you’re in Post. You can click on the different buttons to filter out the kind of post. Some look for teams, others are looking for members. You can now also add a post. Click that button. Once you make that post, you’ll be be brought back to the posts, including yours. 


Note that you can respond to posts as well. Try it. It will go into the inbox of some other user. To find that user (you can either backend query for their name/id in Student) you can put in a bit of work and find their login info to see that your response to their post ended up in their mailbox. 
