from flask import Flask, render_template, url_for, request
from AjaxHandler import AjaxHandler
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item
import json

app = Flask(__name__)

engine = create_engine('postgresql:///catalog')
# engine = create_engine('mysql://andkim:andkim@localhost:3306/catalog', pool_recycle=3600)
Base.metadata.bind = engine

DBSessionMaker = sessionmaker(bind=engine)
#dbSession = DBSession()
""":type: sqlalchemy.orm.Session"""

ajax_handler = AjaxHandler(DBSessionMaker)


@app.route("/")
@app.route("/catalog", methods=["GET", "POST"])
def catalog():
    if request.method == 'POST':
        post_data = request.get_json(silent=True, force=True)
        ajax_handler.posted_data = post_data
        response_data = ajax_handler.processRequest()
        if response_data:
            return render(response_data[0], response_data[1])
        else:
            return False
    else:
        return render_template('catalog.html')


# Helper Functions
def render(template_name, data):
    if template_name:
        return render_template(template_name, data=data)
    else:
        return json.loads(data)


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
