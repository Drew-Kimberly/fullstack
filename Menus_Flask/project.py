__author__ = 'Drew'
from flask import Flask, render_template, request, url_for, redirect, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
import bleach

app = Flask(__name__)


engine = create_engine('postgresql:///menus')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route('/') #Decorators that wrap below function in the app.route() function
@app.route('/restaurants/<int:restaurant_id>/') #Passed in via the restaurantMenu function param
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter(MenuItem.restaurant_id == restaurant_id)

    return render_template('menu.html', restaurant=restaurant, items=items)


# Task 1: Create route for newMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET','POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(
                name = request.form['name'],
                restaurant_id = restaurant_id
        )
        session.add(newItem)
        session.commit()
        flash("New Menu Item Created!")
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id = restaurant_id)


# Task 2: Create route for editMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    #Grab the menu item being edited
    menuItem = session.query(MenuItem).filter_by(id = menu_id).one()

    if request.method == 'POST':
        #Update information in database
        if request.form["name"]:
            menuItem.name = request.form["name"]
        session.add(menuItem)
        flash("Menu Item Edited")
        session.commit()

        #Return to restaurant page
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('editmenuitem.html',
                               restaurant_id = restaurant_id,
                               menu_id = menu_id,
                               menuItem_name = menuItem.name)


# Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    menuItem = session.query(MenuItem).filter_by(id=menu_id).one()

    #Delete the menu item from the DB on post request
    if request.method == 'POST':
        session.delete(menuItem)
        session.commit()
        flash("Menu Item Deleted")

        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('deletemenuitem.html', menuItem = menuItem)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
