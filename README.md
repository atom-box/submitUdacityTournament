(This was developed in another repo, see the long history of my commits at https://github.com/atom-box/mars/tree/master/vagrant/tournament )

V2.0  Tournament.py   November 18, 2017
Program to keep track of players during a Swiss-style tournament
(version 1.0 was previously submitted on Nov 18, 2017 but returned with referee comments)
This program was completed for the Udacity Relational Databases and Full Stack Fundamentals courses  It was written by Evan Genest    

List of Associated Files
-----------------------
tournament_test.py
tournament.sql
tournament.py

General Usage Notes
-----------------------
1.  Requires installing (a) PostgreSQL and (b) psycops2 package for Python
2.  Start by running the sql setup:     $psql tournament
3.  Then run: python tournament_test.py  This will call each of the functions in the tournament.py module.



Description of the database
-----------------------

The database has two initial tables:

name | player_id      match_id  |  winner_id  |  loser_id 
		 | (KEY)      		(KEY)		  |  						| 
==============				====================================
		 |													|							|
		 |													|							|
		 |													|							|

Seven(!) views are generated by the program.   
I did this to maximize readability and ease of altering the details.  
If I had to release this for use, I would condense these into just two views.



Evan Genest can be reached at
-----------------------
email: genest.1 at osu.edu
Twitter: @MisterGenest
github: https://github.com/atom-box/mars/tree/master/vagrant/tournament 





