import math


class Movie:
    """ This class provides a way to store movie related information"""

    def __init__(self, title, duration, year_released, storyline, poster_img_url, youtube_url):
        """
        :param title (str): Title of the movie
        :param duration (int): Duration of the movie in minutes
        :param year_released (str): Year movie was released
        :param storyline (str): Short description of the movie's plot
        :param poster_img_url (str): URL pointing to the movie's poster image
        :param youtube_url (str): URL pointing to the movie's YouTube trailer video
        """
        self.title = title
        self.duration = duration
        self.year_released = year_released
        self.storyline = storyline
        self.poster_img_url = poster_img_url
        self.youtube_url = youtube_url


    def format_duration(self):
        """Returns movie duration in user-friendly format

        Returns the movie's duration as a string in the
        form: "{hours}h {minutes}m"

        Ex: 2h 11m
        """
        num_hours = math.floor(self.duration / 60)
        num_minutes = self.duration % 60
        return str(num_hours) + "h " + str(num_minutes) + "m"

