-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

--Create tournament db
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament

--Create the players table
CREATE TABLE players (
    player_id       serial PRIMARY KEY,
    player_name     text NOT NULL,
    had_bye         boolean NOT NULL DEFAULT FALSE
);

--Create the matches table
--TODO: Add match_id primary key to matches table
CREATE TABLE matches (
    match_id        serial PRIMARY KEY,
    player1_id      integer REFERENCES players(player_id),
    player2_id      integer REFERENCES players(player_id),
    winner          integer CHECK (winner IN (player1_id, player2_id)) --PlayerID of winner
);

--Returns the total number of matches opponents of a given player have won
CREATE OR REPLACE FUNCTION get_opponent_match_wins(player_id INT) RETURNS BIGINT AS $$
  SELECT COUNT(*) FROM matches WHERE winner IN
    (select
      CASE player1_id
        WHEN player_id THEN player2_id
        ELSE player1_id
      END AS opponent
    FROM matches WHERE player1_id=player_id OR player2_id=player_id);
$$ LANGUAGE SQL;

--Create the player standings view
CREATE VIEW player_standings AS
    SELECT p.player_id, p.player_name, wc.wins, mc.num_matches, wc.omw
    FROM players p
    JOIN
    (
        SELECT p.player_id, p.player_name, COUNT(m.winner) AS wins, get_opponent_match_wins(p.player_id) AS omw FROM
           players p LEFT JOIN matches m ON p.player_id=m.winner
             GROUP BY p.player_id
    ) AS wc
    ON p.player_id=wc.player_id
    LEFT JOIN
    (
        SELECT p.player_id, p.player_name, COUNT(m.winner) AS num_matches FROM
          players p LEFT JOIN matches m ON (p.player_id=m.player1_id) OR (p.player_id=m.player2_id)
            GROUP BY p.player_id
    ) AS mc
    ON p.player_id=mc.player_id
    ORDER BY wins DESC, omw DESC;

--Checks to see if 2 players have already played eachother in the tournament.
--Returns 1 if they have already played, 0 if they have not
CREATE OR REPLACE FUNCTION check_for_rematch(player_id INT, opponent_id INT) RETURNS INT AS $$
  SELECT
    CASE WHEN EXISTS
      (SELECT * FROM matches WHERE (player1_id = $1 AND player2_id = $2) OR (player1_id = $2 AND player2_id = $1))
      THEN 1
      ELSE 0
    END;
$$ LANGUAGE SQL;