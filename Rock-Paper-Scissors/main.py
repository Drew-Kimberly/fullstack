#!/usr/bin/env python

"""main.py - This file contains handlers that are called by taskqueue and/or
cronjobs."""

import webapp2
from google.appengine.api import mail, app_identity
from models.Game import Game


class SendReminderEmail(webapp2.RequestHandler):
    def get(self):
        """Send a reminder email to each User with incomplete active games.
        Called every 24 hours using a cron job"""
        app_id = app_identity.get_application_id()
        games = Game.query(Game.game_over == False)
        users = []

        for game in games:
            users.append(game.user.get())

        for user in users:
            subject = 'This is a reminder!'
            body = 'Hello {}, come back and finish your game of Rock, Paper, Scissors!'.format(user.displayName)
            mail.send_mail('noreply@{}.appspotmail.com'.format(app_id),
                           user.email,
                           subject,
                           body)


app = webapp2.WSGIApplication([
    ('/crons/send_reminder', SendReminderEmail),
], debug=True)
