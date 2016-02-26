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
@app.route('/catalog')
def catalog():
    categories = session.query(Category).all()
    latest_items = session.query(Item).all()

    return render_template('catalog.html', categories=categories, latest_items=latest_items)


@app.route('/item/new', methods=['GET', 'POST'])
def newItem():
    if request.method == 'POST':
        if request.form["name"] != "" and request.form["category"] != "":
            category = Category(name = request.form["category"])
            #Check for existing category name in database
            if not session.query(Category).filter_by(name=category.name).first():
                session.add(category)
                session.flush() #Flush change to the database in order to assign category_id

            newItem = Item(
                name = request.form["name"],
                description = request.form["description"],
                category_id = category.category_id
            )
            session.add(newItem)
            session.commit()

        return redirect(url_for("catalog"))
    else:
        categories = session.query(Category).all()
        return render_template('newitem.html', categories=categories)


@app.route('/item/<int:item_id>')
def viewItem(item_id):
    return "Item view when a user is not authenticated."


@app.route('/categories/<int:category_id>')
def catalogCategory(category_id):
    return "Lists all items within a given category"


@app.route('/categories/new') #Is this needed?
def newCategory():
    return "Form to add a new category into the db."


@app.route('/categories/<int:category_id>/edit')
def editCategory(category_id):
    return "Form to edit an existing category."


@app.route('/categories/<int:category_id>/delete')
def deleteCategory(category_id):
    return "Delete an exisiting category here"


@app.route('/categories/<int:category_id>/items/<int:item_id>')
def catalogItem(category_id, item_id):
    return "Lists the description of an item."


@app.route('/item/<int:item_id>/edit', methods=['GET', 'POST'])
@app.route('/categories/<int:category_id>/items/<int:item_id>/edit', methods=['GET', 'POST'])
def editItem(item_id, category_id=None):
    item = session.query(Item).filter_by(item_id = item_id).one()

    if request.method == 'POST':
        return "Form to edit an exisiting item"
    else:
        return render_template("edititem.html", item=item)




@app.route('/categories/<int:category_id>/items/<int:item_id>/delete')
def deleteItem(category_id, item_id):
    return "Form to delete an existing item"

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 8000)