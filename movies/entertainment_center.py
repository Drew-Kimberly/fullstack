import media, fresh_tomatoes

#Create Movie instances to be rendered by fresh_tomatoes.py

dark_knight_rises = media.Movie("The Dark Knight Rises", 165, "2012",
                                "Batman squares off in an epic battle against the evil Bane",
                                "https://upload.wikimedia.org/wikipedia/en/8/83/Dark_knight_rises_poster.jpg",
                                "https://www.youtube.com/watch?v=g8evyE9TuYk")

usual_suspects = media.Movie("The Usual Suspects", 108, "1995",
                             "In a world where nothing is what it seems, you've got to look beyond...",
                             "https://upload.wikimedia.org/wikipedia/en/9/9c/Usual_suspects_ver1.jpg",
                             "https://www.youtube.com/watch?v=oiXdPolca5w")

other_guys = media.Movie("The Other Guys", 116, "2010",
                         "Two mismatched New York City detectives seize an opportunity to step up",
                         "https://upload.wikimedia.org/wikipedia/en/6/6b/Other_guys_poster.jpg",
                         "https://www.youtube.com/watch?v=D6WOoUG1eNo")

dodgeball = media.Movie("Dodgeball", 93, "2004",
                        "Grab life by the ball",
                        "https://upload.wikimedia.org/wikipedia/en/7/70/Movie_poster_Dodgeball_A_True_Underdog_Story.jpg",
                        "https://www.youtube.com/watch?v=W-XbDZUnUmw")

step_brothers = media.Movie("Step Brothers", 106, "2008",
                            "They grow up so fast",
                            "https://upload.wikimedia.org/wikipedia/en/d/d9/StepbrothersMP08.jpg",
                            "https://www.youtube.com/watch?v=ANjenc4W1_Q")

guardians = media.Movie("Guardians of the Galaxy", 122, "2014",
                        "The galaxy is in good hands",
                        "https://upload.wikimedia.org/wikipedia/en/8/8f/GOTG-poster.jpg",
                        "https://www.youtube.com/watch?v=B16Bo47KS2g")

entourage = media.Movie("Entourage", 104, "2015",
                        "Dream large. Live larger.",
                        "https://upload.wikimedia.org/wikipedia/en/d/df/Entourage_film_2015_poster.jpg",
                        "https://www.youtube.com/watch?v=UkziCQtI_6U")

office_space = media.Movie("Office Space", 89, "1999",
                           "Work sucks",
                           "https://upload.wikimedia.org/wikipedia/en/8/8e/Office_space_poster.jpg",
                           "https://www.youtube.com/watch?v=_IwzZYRejZQ")

american_psycho = media.Movie("American Psycho", 102, "2000",
                              "Killer looks",
                              "https://upload.wikimedia.org/wikipedia/en/6/63/Americanpsychoposter.jpg",
                              "https://www.youtube.com/watch?v=2GIsExb5jJU")

toy_story = media.Movie("Toy Story", 81, "1995",
                        "A story of a boy and his toys that come to life.",
                        "https://upload.wikimedia.org/wikipedia/en/1/13/Toy_Story.jpg",
                        "https://www.youtube.com/watch?v=KYz2wyBy3kc")

avatar = media.Movie("Avatar", 178, "2009",
                     "A marine on an alien planet.",
                     "https://upload.wikimedia.org/wikipedia/en/b/b0/Avatar-Teaser-Poster.jpg",
                     "https://www.youtube.com/watch?v=d1_JBMrrYw8")

space_jam = media.Movie("Space Jam", 100, "1996",
                        "Michael Jordan and Bugs Bunny team up to ball out.",
                        "https://upload.wikimedia.org/wikipedia/en/1/14/Space_jam.jpg",
                        "https://www.youtube.com/watch?v=u7AYd8uGG6E")

school_of_rock = media.Movie("School of Rock", 109, "2003",
                             "Learning through the power of rock n roll!",
                             "https://upload.wikimedia.org/wikipedia/en/1/11/School_of_Rock_Poster.jpg",
                             "https://www.youtube.com/watch?v=XCwy6lW5Ixc")

hot_rod = media.Movie("Hot Rod", 88, "2007",
                      "Smack destiny in the face.",
                      "https://upload.wikimedia.org/wikipedia/en/7/7f/Hot-rod-poster.jpg",
                      "https://www.youtube.com/watch?v=DhdrA9qz79o")

inception = media.Movie("Inception", 148, "2010",
                        "Have fun trying to figure out if it's still spinning.",
                        "https://upload.wikimedia.org/wikipedia/en/7/7f/Inception_ver3.jpg",
                        "https://www.youtube.com/watch?v=66TuSJo4dZM")

movies = [dark_knight_rises, usual_suspects, other_guys, dodgeball, step_brothers, guardians, entourage, office_space,
          american_psycho,toy_story, avatar, space_jam, school_of_rock, hot_rod, inception]

fresh_tomatoes.open_movies_page(movies)
