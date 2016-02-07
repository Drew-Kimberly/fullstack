from flask import Flask, render_template, request, url_for, redirect, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item

app = Flask(__name__)

engine = create_engine('postgresql:///catalog')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route('/')
def catalog():
    categories = session.query(Category).all()
    latest_items = session.query(Item).all()

    return render_template('catalog.html', categories=categories, latest_items=latest_items)


if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 8000)