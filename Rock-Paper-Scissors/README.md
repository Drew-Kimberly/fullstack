#Rock Paper Scissors API

## Set-Up Instructions:
1.  Update the value of application in app.yaml to the app ID you have registered
 in the App Engine admin console and would like to use to host your instance of this application.
1.  This app requires Google+ Authentication. Update the value of WEB_CLIENT_ID in settings.py
with your own Client ID from the Google API Console.
1.  Run the app with the devserver using dev_appserver.py DIR, and ensure it's
 running by visiting the API Explorer - by default localhost:8080/_ah/api/explorer.
1.  (Optional) Generate your client library(ies) with the endpoints tool.
 Deploy your application.
 

##Game Description:
Rock Paper Scissors is a timeless classic. This application allows a user to play
rock paper scissors games against a computer opponent. A game can contain 1, 3, 5,
or 7 rounds. The game is a "best-of" series, where one player must win the majority
of rounds to win the game. For example, if the game is set to 5 rounds - a player
must win 3 rounds to win the game.

Gameplay is straightforward. Each player can make 1 of 3 moves per
round: 'Rock', 'Paper', or 'Scissors'. Each move beats exactly 1 other move.
The breakdown of this is as follows:
- Rock beats Scissors
- Scissors beats Paper
- Paper beats Rock

If both players play the same move, a tie is declared. In this case, the round is not
considered complete and both players must each make another move against eachother.
Once the user wins/loses, the round is over and the round result is recorded.
If an overall game winner has not been established, the players begin another round,
and keep doing so until the game is completed.

The application saves and associates the result of each game with the participating
user to maintain an overall Win/Loss record. The margin of victory is also saved
for every game. User's overall margin of victory is the metric used to rank
the users in the system against eachother. The greater your margin of victory,
the better your rank in the system.

The application allows many different users to play many different Rock Paper Scissor
games simultaneously. Users have the ability to view round-by-round results of their
own completed or active games using the `get_game_history` endpoint. Users can also
view how their all-time and single-game performances compare to other users' with
the `get_high_scores` and `get_user_rankings` endpoints respectively. The user's games
can be retrieved or played by using the path parameter `urlsafe_game_key`.

<i>A user must authenticate using a Google+ sign-in in order to play!</i>


##Files Included:
 - api.py: Contains all endpoints for the application.
 - app.yaml: App configuration.
 - settings.py: User configuration settings.
 - cron.yaml: Cronjob configuration.
 - main.py: Handler for taskqueue handler.
 - Game.py: Definition for Game entity.
 - Score.py: Definition for Score entity.
 - User.py: Definition for User entity.
 - GameHandler.py: Service class containing the game logic pertinent to the Game entity.
 - ScoreHandler.py: Service class containing the game logic pertinent to the Score entity.
 - UserHanlder.py: Service class containing the game logic pertinent to the User entity.
 - utils.py: Helper functions used across the application.


##Endpoints Included:
 - **save_user**
    - Path: 'user'
    - Method: POST
    - Auth Required: TRUE
    - Parameters: display_name (optional)
    - Returns: UserForm
    - Description: Creates a new user profile if the sign in email does not exist in the system.
        Otherwise, updates the user profile's information if there is a change.

 - **get_user**
    - Path: 'user'
    - Method: GET
    - Auth Required: TRUE
    - Parameters: None
    - Returns: UserForm
    - Description: Returns the current authenticated User profile.
    
 - **new_game**
    - Path: 'game'
    - Method: POST
    - Auth Required: TRUE
    - Parameters: total_rounds
    - Returns: GameForm with initial game state.
    - Description: Creates a new Rock-Paper-Scissors Game with the provided number of rounds
     for the current authenticated User. The parameter total_rounds must be an integer within the set (1, 3, 5, 7).
     
 - **get_game**
    - Path: 'game/{urlsafe_game_key}'
    - Method: GET
    - Auth Required: TRUE
    - Parameters: urlsafe_game_key
    - Returns: GameForm with current game state.
    - Description: Returns the current state of a game.
    
 - **play_round**
    - Path: 'game/{urlsafe_game_key}'
    - Method: PUT
    - Auth Required: TRUE
    - Parameters: urlsafe_game_key, move
    - Returns: GameForm with new game state.
    - Description: Accepts a Rock-Paper-Scissors 'move' ('ROCK', 'PAPER', or 'SCISSORS') and plays a round of the
    game using a randomized move by the computer opponent. The updated state of the game is then returned.
    If this causes a game to end, a corresponding Score entity will be created.
    Users must be the owner the game they are requesting to play a round of, and the game must currently be active.
    
 - **get_scores**
    - Path: 'scores'
    - Method: GET
    - Auth Required: TRUE
    - Parameters: None
    - Returns: ScoreForms.
    - Description: Returns all Scores from all users in the database (unordered).
    
 - **get_user_scores**
    - Path: 'scores/user'
    - Method: GET
    - Auth Required: TRUE
    - Parameters: email
    - Returns: ScoreForms. 
    - Description: Returns all Scores recorded by the provided player (unordered).
    Will raise a NotFoundException if the User does not exist.

- **get_user_games**
    - Path: 'user/games'
    - Method: GET
    - Auth Required: TRUE
    - Parameters: None
    - Returns: GameForms
    - Description: Returns all of the currently authenticated User's active games (unordered).

- **cancel_game**
    - Path: 'game/{urlsafe_game_key}'
    - Method: DELETE
    - Auth Required: TRUE
    - Parameters: urlsafe_game_key
    - Returns: Message that the given game was successfully cancelled.
    - Description: Cancels the game given by urlsafe_game_key. The game must belong to the current
    authenticated user and be an active game.

- **get_high_scores**
    - Path: '/highscores'
    - Method: 'GET'
    - Auth Required: TRUE
    - Parameters: number_of_results
    - Returns: ScoreForms
    - Description: By default returns a list of all Score entities in the database,
    ordered descending by the User's margin of victory of the game. The parameter
    number_of_results can be used to limit the number of Scores returned.

- **get_user_rankings**
    - Path: '/user_rankings'
    - Method: GET
    - Auth Required: TRUE
    - Parameters: None
    - Returns: UserRankForms
    - Description: Returns a list of all User entities in the database,
    ordered descending by the User's total margin of victory, which is returned
    as the `total_victory_margin` field for each User.

- **get_game_history**
    - Path: 'game/{urlsafe_game_key}/history'
    - Method: GET
    - Auth Required: TRUE
    - Parameters: urlsafe_game_key
    - Returns: GameHistoryForm
    - Description: Returns the round-by-round result of an active or completed Game.


##Models Included:
 - **User**
    - Stores unique email, a display name, and user statistics.
    
 - **Game**
    - Stores unique game states. Associated with User model via KeyProperty.
    
 - **Score**
    - Records completed games. Associated with Users model via KeyProperty.
    
##Forms Included:
 - **UserForm**
    - Representation of a User entity.
    - Fields:
        - email
        - displayName
        - num_wins
        - num_losses
        - toatal_victory_margin

 - **UserMiniForm**
    - Used to display updateable information about a User entity
    - Fields:
        - displayName

 - **GameForm**
    - Representation of a Game's state
    - Fields:
        - urlsafe_key
        - total_rounds
        - remaining_rounds
        - game_over
        - user_email
        - user_name
        - user_last_move
        - cpu_last_move
        - user_won_last_round
        - total_ties
        - user_wins
        - cpu_wins

 - **GameForms**
    - Multiple GameForm container.

 - **NewGameForm**
    - Used to create a new game
    - Fields:
        - total_rounds

 - **PlayRoundForm**
    - Inbound form to play a round.
    - Fields
        - move

 - **RoundHistoryForm**
    - Summarizes an already completed round.
    - Fields:
        - user_move
        - cpu_move
        - user_won
        - is_tie

 - **GameHistoryForm**
    - Multiple RoundHistoryForm container

 - **ScoreForm**
    - Representation of a completed game's Score.
    - Fields:
        - user_email
        - user_name
        - date
        - won
        - victory_margin

 - **ScoreForms**
    - Multiple ScoreForm container.

- **UserRankForm**
    - Representation of individual user ranking information.
    - Fields:
        - email
        - displayName
        - total_victory_margin

- **UserRankForms**
    - Multiple UserRankForm container.

 - **StringMessage**
    - General purpose String container.


##Cron Jobs:

 - **Email Notifications**
    - SendReminderEmail
        - Implemented in: main.py
        - Configured in: cron.yaml
        - Description: Sends a reminder email to each User with incomplete active games.
        Called every day at 8:00PM ET using a cron job.