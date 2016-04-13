from flask import Flask, render_template, request, url_for, redirect, flash
from util import ItemConverter, CategoryConverter
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item

app = Flask(__name__)

app.url_map.converters['item'] = ItemConverter
app.url_map.converters['category'] = CategoryConverter

engine = create_engine('postgresql:///catalog')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()
""":type: sqlalchemy.orm.Session"""


@app.route('/')
@app.route('/catalog')
def catalog():
    categories = session.query(Category).all()
    items = session.query(Item).all()

    return render_template('catalog.html', categories=categories, items=items)


@app.route('/catalog/newItem', methods=['GET', 'POST'])
def newItem(category_id=None):
    if request.method == 'POST':
        if request.form["name"] != "" and request.form["category"] != "":
            newItem = Item(
                name=request.form["name"],
                description=request.form["description"],
                category_id=request.form["category"]
            )
            session.add(newItem)
            session.commit()

        return redirect(url_for("catalog"))
    else:
        if category_id:
            categories = session.query(Category).filter_by(category_id=category_id).first()
            categories = [categories]
        else:
            categories = session.query(Category).all()
        return render_template('newitem.html', categories=categories, category_id=category_id)


# @app.route('/catalog/<string:category_name>/<string:item_name>')
# @app.route('/catalog/<item.category.name>/<item.name>')
# def viewItem(category_name, item_name, item_id):
#     item = session.query(Item).filter_by(item_id=item_id).first()
#     return render_template("viewitem.html", item=item)
@app.route('/catalog/<category:category>/<item:item>')
def viewItem(item, category):
    return render_template("viewitem.html", item=item)


@app.route('/catalog/<category:category>/<item:item>/edit', methods=['GET', 'POST'])
def editItem(item, category):
    if request.method == 'POST':

        # Update information in database
        if request.form["name"] != "" and request.form["category"] != "":
            item.category_id = request.form["category"]
            item.name = request.form["name"]
            item.description = request.form["description"]

            session.add(item)
            session.commit()

        # Return to the view item page
        return redirect(url_for('viewItem', item=item, category=item.category))
    else:
        # Render edit item page on GET request
        categories = session.query(Category).all()
        return render_template("edititem.html", item=item, categories=categories)


@app.route('/catalog/<category:category>/<item:item>/delete', methods=['GET', 'POST'])
def deleteItem(item, category):
    if request.method == "POST":

        # Delete the item
        session.delete(item)
        session.commit()

        return redirect(url_for('catalog'))
    else:
        # Render delete item page on GET request
        return render_template("deleteitem.html", item=item)


@app.route('/catalog/<category:category>')
def viewCategory(category):
    items = session.query(Item).filter_by(category_id=category.category_id).all()
    return render_template("viewcategory.html", category=category, items=items)


@app.route('/catalog/newCategory', methods=['GET', 'POST'])
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


@app.route('/catalog/<category:category>/edit', methods=['GET', 'POST'])
def editCategory(category):
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


@app.route('/catalog/<category:category>/delete', methods=['GET', 'POST'])
def deleteCategory(category):
    if request.method == 'POST':
        items = session.query(Item).filter_by(category_id=category.category_id).all()
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
