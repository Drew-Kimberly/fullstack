Swiss-System Tournament Simulator 1.1 11/16/2015

GENERAL INFORMATION
--------------------

 - This is a basic database-backed Swiss-style tournament simulator, which will simulate a tournament
 	with a given number of registered contestants and display the tournament results. 

 - The simulator supports any number of contestants beyond 2. Byes will be assigned for tournaments
 	with an odd number of contestants, ensuring that no player can receive more than 1 bye per
 	tournament.

 - Rematches between any 2 players within a tournament are *for the most part* prevented. In some
 	cases, tournaments with a total number of players that are odd or even but not a power of 2,
 	will have the chance of having players matched against eachother for a second time.

 - The tournament rankings are determined by total number of wins. Given the case where two or more
 	players are tied with the same number of total wins, the simulator uses the total number of wins
 	by players a given player has played against (Opponent Match Wins) as the tie-breaking heuristic.


USAGE NOTES
--------------

- Requirements:
	- Python2
	- PostGreSQL
	- PsycoPg2

- If creating local database instance, must create new PostGreSQL database named "tournament"

- From the command prompt, change directory to the "tournament" directory (the folder containing this file)

- Execute the command: python tournament_test.py [num_players]

	Where num_players is an integer value greater than 2, which represents the total number of
	registered contestants to simulate the tournament with.
	If tournament_test.py is executed with no value entered for num_players, the program will
	simulate a tournament with 8 registered contestants.


GENERAL REFERENCES
---------------------

- https://docs.python.org/2/
- http://initd.org/psycopg/docs/
- http://www.postgresql.org/docs/


AUTHORS
----------

Drew Kimberly, with help from the Udacity team