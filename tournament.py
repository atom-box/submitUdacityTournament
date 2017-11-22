#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    # I plan to use this within the other routines
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    db = connect()
    c = db.cursor()
    QUERY = 'TRUNCATE TABLE matches;'
    c.execute(QUERY)
    db.commit()
    db.close()
    """Remove all the match records from the database."""


def deletePlayers():
    db = connect()
    c = db.cursor()
    QUERY = 'TRUNCATE TABLE players;'
    c.execute(QUERY)
    db.commit()
    db.close()
    """Remove all the player records from the database."""


def countPlayers():
    handleBarMoustache = connect()
    swearer = handleBarMoustache.cursor()
    QUERY = 'SELECT COUNT(*) FROM players;'
    swearer.execute(QUERY)
    x = swearer.fetchall()
    handleBarMoustache.close()
    return int(x[0][0])

    """Returns the number of players currently registered."""


def registerPlayer(name):
    HAN_SOLO = connect()
    c = HAN_SOLO.cursor()
    QUERY = "INSERT INTO players (name) VALUES (%s);"
    DATA = (name, )
    c.execute(QUERY, DATA)
    HAN_SOLO.commit()
    HAN_SOLO.close()

    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """


def playerStandings():
    h = connect()
    c = h.cursor()
    QUERY_CLEAR = '''
    DROP VIEW IF EXISTS w, l, pw, pwl, pwl2, s, inwm;
    '''

    QUERY_W = """
    CREATE VIEW w AS
    SELECT matches.winner_id, count(*)::smallint as wins
    FROM matches GROUP BY winner_id;
    """
    QUERY_L = """
        CREATE VIEW l AS
        SELECT matches.loser_id, count(*)::smallint as losses
        FROM matches GROUP BY loser_id;
    """
    QUERY_PW = """
        CREATE VIEW pw AS
        SELECT players.name, players.player_id, W.wins
        FROM players LEFT JOIN W
        ON players.player_id = W.winner_id;
    """
    QUERY_PWL = """
        CREATE VIEW pwl AS
        SELECT PW.name, PW.player_id, PW.wins, L.losses
        FROM PW LEFT JOIN L
        ON PW.player_id = L.loser_id;
    """
    QUERY_PWL2 = """
        CREATE VIEW pwl2 AS
        SELECT name, player_id,
        CASE
            WHEN wins ISNULL
                THEN 0
            ELSE
                wins END,
        CASE
            WHEN losses ISNULL
                THEN 0
            ELSE
                losses END
        FROM PWL;
    """
    QUERY_S = """
        CREATE VIEW s AS
        SELECT player_id, wins + losses AS STARTS
        FROM pwl2;
    """
    QUERY_INWM = """
        SELECT pwl2.player_id,
        pwl2.name, pwl2.wins,
        s.starts
        FROM pwl2 JOIN s
        ON pwl2.player_id =s.player_id;
    """
    c.execute(QUERY_CLEAR)
    c.execute(QUERY_W)
    c.execute(QUERY_L)
    c.execute(QUERY_PW)
    c.execute(QUERY_PWL)
    c.execute(QUERY_PWL2)
    c.execute(QUERY_S)
    c.execute(QUERY_INWM)
    theStuff = c.fetchall()  # c.fetchall()
    h.commit()
    h.close()
    return theStuff
    """
    Returns a list of the players and their win records, sorted by wins.
    The first entry in the list should be the player in first place, or 
    a player tied for first place if there is currently a tie.
    """


def reportMatch(winner, loser):
    h = connect()
    c = h.cursor()
    QUERY1 = "INSERT INTO matches (winner_id, loser_id) VALUES (%s, %s);"
    DATA_WINNER = (winner,)
    DATA_LOSER = (loser,)
    c.execute(QUERY1, (DATA_WINNER, DATA_LOSER))
    h.commit()
    h.close()
    return


def swissPairings():
    playerStandings()  # creates views that are pre-requisite to QUERY's below.
    h = connect()  # subtle bug! function PLAYERSTANDINGS should reopen!
    c = h.cursor()
    QUERY0 = '''
    DROP VIEW IF EXISTS players2, players3;
    '''
    QUERY1 = '''
        CREATE VIEW players2 AS
        SELECT player_id, name, wins
        FROM pwl2 ORDER BY wins DESC;
    '''
    c.execute(QUERY1)

    QUERY2 = '''
        CREATE VIEW players3 AS
        SELECT player_id, name, wins,
        row_number() OVER (ORDER BY wins DESC)
        AS counter
        FROM players2  ;
    '''
    QUERY3 = '''
        SELECT a.player_id, a.name, b.player_id, b.name
        FROM players3 as a, players3 AS b
        WHERE a.counter+1 = b.counter AND (a.counter%2=1);
    '''
    c.execute(QUERY0)
    c.execute(QUERY1)
    c.execute(QUERY2)
    c.execute(QUERY3)
    rawAll = c.fetchall()
    return rawAll
    """Returns a list of pairs of players for the next round of a match.
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
    """
