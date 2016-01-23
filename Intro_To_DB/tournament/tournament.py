#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import psycopg2.extras
import random


def connect(db_name="tournament"):
    """Connect to the PostgreSQL database.  Returns a database connection and a database cursor."""
    try:
        conn = psycopg2.connect("dbname={}".format(db_name))
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        return conn, cur
    except:
        print("Error connecting to the " + db_name + " database.")


def deleteMatches():
    """Remove all the match records for all existing tournaments from the database."""
    conn, cur = connect()
    query = "TRUNCATE matches CASCADE;"
    try:
        cur.execute(query)
    except:
        print("Error encountered deleting all matches.")
    conn.commit()
    conn.close()


def deletePlayers():
    """Removes all player records from the database."""
    conn, cur = connect()
    query = "TRUNCATE players CASCADE;"
    try:
        cur.execute(query)
    except:
        print("Error encountered deleting all players")
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn, cur = connect()
    query = "SELECT count(*) AS player_count FROM players;"
    try:
        cur.execute(query)
    except:
        print("Error encountered when selecting player count from players table")
    num_players = cur.fetchone()
    conn.close()
    return num_players['player_count']


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn, cur = connect()
    query = "INSERT INTO players (player_name) VALUES (%s);"
    param = (name,)
    try:
        cur.execute(query, param)
    except:
        print("Error encountered when inserting player " + name + " into the database")
    conn.commit()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins
        then total number of opponent wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn, cur = connect()
    query = "SELECT * FROM player_standings;"
    try:
        cur.execute(query)
    except:
        print("Error encountered when selecting player standings from the database")
    player_standings = cur.fetchall()
    conn.close()

    standings = []
    for player in player_standings:
        standings.append((player['player_id'], player['player_name'],
                          (int)(player['wins']), (int)(player['num_matches'])))
    return standings


def reportMatch(player1, player2, winner = None):
    """Records the outcome of a single match between two players.
       If no winner provided, randomly generates the match outcome.

    Args:
      player1:  the id number of the 1st player in the match
      player2:  the id number of the 2nd player in the match
      winner (optional):   the id number of the winning player
    """
    #Check for Bye matchup (player1=player2)
    bye_match = False
    if player1 == player2:
        winner = player1
        bye_match = True

    #Generate random winner if no winner param is passed in
    if winner is None:
        rand = random.random()
        if rand < 0.5:
            winner = player1
        else:
            winner = player2

    conn, cur = connect()
    #Insert record of match
    query = """INSERT INTO matches (player1_id, player2_id, winner)
                VALUES (%s, %s, %s)"""
    params = (player1, player2, winner,)
    try:
        cur.execute(query, params)
    except:
        print("Error encountered when inserting match record into the database")

    #Save record of player having a bye in Players table
    if bye_match:
        query = "UPDATE players SET had_bye = TRUE WHERE player_id = %s;"
        param = (player1,)
        try:
            cur.execute(query, param)
        except:
            print("Error encountered when updating player's Bye round status.")
    conn.commit()
    conn.close()

 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    standings = playerStandings()
    player_count = len(standings)
    pairings = []

    if standings[0][3] == 0: #First round of tourney - Create random pairings
        unmatched_players = player_count
        for i in range(player_count // 2):
            match_player1 = standings.pop(random.randrange(unmatched_players))
            match_player2 = standings.pop(random.randrange(unmatched_players - 1))
            pairings.append((match_player1[0], match_player1[1], match_player2[0], match_player2[1]))
            unmatched_players -= 2

        if unmatched_players > 0: #Odd Number of Contestants - Give last unmatched a player a bye (paired against himself)
            pairings.append((standings[0][0], standings[0][1], standings[0][0], standings[0][1]))
    else:
        #Check for odd number of players first to see if we need to assign a bye
        if player_count % 2 > 0:
            bye_assigned = False
            #Start from bottom of standings and continue up until player who has yet to have a Bye is found
            iter = player_count - 1
            while not bye_assigned:
                if not checkForBye(standings[iter][0]):
                    #Assign Bye by pairing the player against himself and removing him from the standings list
                    bye_player = standings.pop(iter)
                    pairings.append((bye_player[0], bye_player[1], bye_player[0], bye_player[1]))
                    bye_assigned = True
                else:
                    iter -= 1

        #Match adjacent players in player standings (if rematch, moves to the next opponent until new match is found)
        #This method prevents most tournaments from having a rematch, but is not a guarantee.
        #Hence, the try/except block eats the out of range error and allows a rematch in the tourney to occur.
        #For implementing mathematically sound anti-rematch measures, see:
        #https://www.leaguevine.com/blog/18/swiss-tournament-scheduling-leaguevines-new-algorithm/
        for i in range(0, player_count // 2):
            new_match = False
            j = 1
            while not new_match:
                try:
                    if checkForRematch(standings[0][0], standings[j][0]) == 0:
                        new_match = True
                    else:
                        j += 1
                except:
                    j = j-1
                    new_match = True

            #When we have a match - add them as a pairing and remove the 2 players from the standings list
            match_player2 = standings.pop(j)
            match_player1 = standings.pop(0)
            pairings.append((match_player1[0], match_player1[1], match_player2[0], match_player2[1]))

    return pairings


def checkForRematch(player_id, opponent_id):
    """Checks to see if 2 players have already played each other in the tournament.

    :param player_id: PlayerID of the first player, integer.
    :param opponent_id: PlayerID of the second player, integer.
    :return: Returns an integer representing whether or not the 2 players
             have had a match record already in the tournament.
             Returns 0, if they have not.
             Returns 1, if there is a match record in existence.
    """
    conn, cur = connect()
    query = "SELECT check_for_rematch(%s, %s);"
    params = (player_id, opponent_id,)
    try:
        cur.execute(query, params)
    except:
        print("Error encountered when checking if playerId:" + str(player_id) +
              " has already played opponentId:" + str(opponent_id))
    isRematch = cur.fetchone()
    conn.close()
    return int(isRematch[0])


def checkForBye(player_id):
    """Checks to see if a given player has already had a bye within the tournament.

    :param player_id: PlayerID of the player we're checking
    :return: Boolean value representing whether or not the player had a bye
             0 - No bye
             1 - Bye
    """
    conn, cur = connect()
    query = "SELECT had_bye FROM players WHERE player_id = %s;"
    param = (player_id,)
    try:
        cur.execute(query, param)
    except:
        print("Error encountered when checking Bye status for PlayerId: " + str(player_id))

    isBye = cur.fetchone()
    conn.close()
    return bool(isBye[0])


