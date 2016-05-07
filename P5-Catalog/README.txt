MyCatalog 1.1 4/18/2016

GENERAL INFORMATION
--------------------

 - My Catalog is a basic catalog web application, displaying categorized items to the user.

 - The item form has additional functionality which allows the user to upload an image to better
    show off a given item.

 - An unauthenticated user visiting the site can view the different categories and items
    that are in each category.

 - A user with a Google+ or Facebook account can sign in to the application using these 3rd-party
    providers. Once authenticated, the user can choose to add, edit, or delete categories and items.
    However, the site contains a local permissions system which allows an authenticated user to
    edit/delete only those categories and items that were created by him/her.

 - The site also contains an API endpoint, which returns all the data within the catalog
    in JSON format.


USAGE GUIDE
--------------

1 - Requirements:
	- Python 2
	- PostgreSQL
	Python Libraries (install with pip):
	    - Flask
	    - SQLAlchemy
	    - werkzeug
	    - OAuth2Client
	    - json
	    - httplib2
	    - requests

2 - From the "catalog" directory, execute: python database_setup.py
    This will create your catalog database with the necessary schema

3 - From the "catalog" directory, execute: python app.py
    This will run the catalog application.

4 - Visit your catalog site at "http://localhost:5000" or "http://localhost:5000/catalog".
    You must log in with either a Google+ or Facebook account to create content. The app will run
    until you stop the app.py process running the terminal.

5 - While app.py is running, visit "http://localhost:5000/catalog/api/getcatalog/json" in your browser
    (or with a REST client), to see the JSON Catalog api response. Much more interesting when you have
    content in the app.


GENERAL REFERENCES
---------------------

- https://docs.python.org/2/
- http://docs.sqlalchemy.org/en/rel_1_0/
- http://flask.pocoo.org/docs/0.10/
- https://api.jquery.com/
- https://alembic.readthedocs.org/en/latest/
- http://stackoverflow.com/


AUTHORS
----------

Drew Kimberly, with help from the Udacity team