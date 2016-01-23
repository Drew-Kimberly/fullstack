#
# Database access functions for the web forum.
# 

import time
import psycopg2
import bleach

## Get posts from database.
def GetAllPosts():
    '''Get all the posts from the database, sorted with the newest first.

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    '''
    # Database connection
    DB = psycopg2.connect("dbname=forum")
    # Open cursor to perform database operations
    cur = DB.cursor()

    # Get all posts sorted by timestamp
    cur.execute('select time, content from posts order by time desc;')

    posts = [{'content': str(bleach.clean(row[1])), 'time': str(row[0])} for row in cur.fetchall()]
    DB.close()
    return posts

## Add a post to the database.
def AddPost(content):
    '''Add a new post to the database.

    Args:
      content: The text content of the new post.
    '''
    # Database connection
    DB = psycopg2.connect("dbname=forum")

    #Open cursor to perform db operations
    cur = DB.cursor()

    #Insert content into posts table and commit the transaction
    cur.execute("INSERT into posts (content) VALUES (%s);", (content,))
    DB.commit()

    #Close the DB connection
    DB.close()

