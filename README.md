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

* Node: There is a small caveat. This process requires a small config change depending on if the developer is running/setting up the database on google cloud or on vagrant. We are working to make this process more general. 

The production data files were all custom generated using generatedata.com for some initial random values. The data was produced to fit the schema, and thus no code was required to extract data into a usable form. The data was made to have many dependencies across tables and thus give interesting results when running our sequel commands. These dependencies were complex to set up the initial data and required human effort rather than code. SQL code was updated after the data was generated to fix some inconsistencies. In addition, the TextStripperForData.java file was used to properly convert and print .csv file text to a .dat usable format.
