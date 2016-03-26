from flask import Flask, render_template, request, url_for, redirect, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item

app = Flask(__name__)

engine = create_engine('postgresql:///catalog')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()
""":type: sqlalchemy.orm.Session"""


@app.route('/')
@app.route('/catalog')
def catalog():
    categories = session.query(Category).all()
    latest_items = session.query(Item).all()

    return render_template('catalog.html', categories=categories, latest_items=latest_items)


@app.route('/item/new', methods=['GET', 'POST'])
@app.route('/categories/<int:category_id>/new', methods=['GET', 'POST'])
def newItem(category_id=None):
    if request.method == 'POST':
        if request.form["name"] != "" and request.form["category"] != "":

            # Check for existing category name in database
            if not session.query(Category).filter_by(name=request.form["category"]).first():
                category = Category(name=request.form["category"])
                session.add(category)
                session.flush()  # Flush change to the database in order to assign category_id
            else:
                category = session.query(Category).filter_by(name=request.form["category"]).first()

            newItem = Item(
                name=request.form["name"],
                description=request.form["description"],
                category_id=category.category_id
            )
            session.add(newItem)
            session.commit()

        return redirect(url_for("catalog"))
    else:
        categories = session.query(Category).all()
        return render_template('newitem.html', categories=categories)


@app.route('/categories/<int:category_id>/items/<int:item_id>')
def viewItem(item_id, category_id):
    item = session.query(Item).filter_by(item_id=item_id).first()
    return render_template("viewitem.html", item=item)


@app.route('/categories/<int:category_id>/items/<int:item_id>/edit', methods=['GET', 'POST'])
def editItem(item_id, category_id):
    item = session.query(Item).filter_by(item_id=item_id).first()
    category = session.query(Category).filter_by(category_id=category_id).first()

    if request.method == 'POST':

        # Update information in database
        if request.form["name"] != "" and request.form["category"] != "":

            # Check if category changed
            if request.form["category"] != category.name:

                # Check if new category is existing category
                if not session.query(Category).filter_by(name=request.form["category"]).first():
                    category = Category(name=request.form["category"])
                    session.add(category)  # Add new category to DB
                    session.flush()  # Flush change to the database in order to assign category_id
                else:
                    category = session.query(Category).filter_by(name=request.form["category"]).first()

                # Assign the item's new category ID
                item.category_id = category.category_id

            item.name = request.form["name"]
            item.description = request.form["description"]

            session.add(item)
            session.commit()

        # Return to the view item page
        return redirect(url_for('viewItem', item_id=item.item_id, category_id=item.category.category_id))
    else:
        # Render edit item page on GET request
        return render_template("edititem.html", item=item)


@app.route('/categories/<int:category_id>/items/<int:item_id>/delete', methods=['GET', 'POST'])
def deleteItem(item_id, category_id):
    item = session.query(Item).filter_by(item_id=item_id).first()
    if request.method == "POST":
        # Delete the item
        session.delete(item)
        session.commit()

        return redirect(url_for('catalog'))
    else:
        # Render delete item page on GET request
        return render_template("deleteitem.html", item=item)


@app.route('/categories/<int:category_id>')
def viewCategory(category_id):
    category = session.query(Category).filter_by(category_id=category_id).first()
    items = session.query(Item).filter_by(category_id=category_id).all()
    return render_template("viewcategory.html", category=category, items=items)


@app.route('/categories/new', methods=['GET', 'POST'])
def newCategory():
    if request.method == 'POST':
        category_name = request.form["name"]
        # Validate the input
        if category_name == "" or session.query(Category).filter_by(name=category_name).first():
            return render_template('newcategory.html')
        else:
            session.add(Category(name=category_name))
            session.commit()
            return redirect(url_for("catalog"))
    else:
        # Render add catalog page on GET request
        return render_template('newcategory.html')


@app.route('/categories/<int:category_id>/edit', methods=['GET', 'POST'])
def editCategory(category_id):
    category = session.query(Category).filter_by(category_id=category_id).first()
    if request.method == 'POST':
        category_name = request.form["name"]

        # Validate the input
        if category_name == "" or \
                        session.query(Category).filter_by(name=category_name).first() and \
                        category.name != category_name:
            return render_template('editcategory.html', category=category)
        else:

            # Don't go to DB if name hasn't changed
            if category.name != category_name:
                category.name = category_name
                session.add(category)
                session.commit()

            return redirect(url_for("catalog"))
    else:
        # Render Edit Category page on GET
        return render_template('editcategory.html', category=category)


@app.route('/categories/<int:category_id>/delete', methods=['GET', 'POST'])
def deleteCategory(category_id):
    category = session.query(Category).filter_by(category_id=category_id).first()
    if request.method == 'POST':
        items = session.query(Item).filter_by(category_id=category_id).all()
        if len(items) > 0:
            for item in items:
                session.delete(item)
        session.delete(category)
        session.commit()

        return redirect(url_for("catalog"))
    else:
        # Render the delete category on GET
        return render_template("deletecategory.html", category=category)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
