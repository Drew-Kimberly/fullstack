import os
from flask import Flask, render_template, url_for, request, jsonify
from AjaxHandler import AjaxHandler
from ImageHelper import ImageHelper
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item
import json

app = Flask(__name__)

engine = create_engine('postgresql:///catalog')
# engine = create_engine('mysql://andkim:andkim@localhost:3306/catalog', pool_recycle=3600)
Base.metadata.bind = engine

DBSessionMaker = sessionmaker(bind=engine)
dbSession = DBSessionMaker()
""":type: sqlalchemy.orm.Session"""


@app.route("/")
@app.route("/catalog", methods=["GET", "POST"])
def catalog():
    if request.method == 'POST':
        ajax_handler = AjaxHandler(dbSession)
        post_data = json.loads(request.form['request_data'])
        if post_data:
            if 'file_data' not in request.files:
                # Normal post request without uploaded file
                ajax_handler.posted_data = post_data
                response_data = ajax_handler.processRequest()  # ResponseData object
                if response_data:
                    return process_response(response_data)
                else:
                    return False
            else:
                # File included in request - first save the file in filesystem
                image_file = request.files['file_data']
                post_data = json.loads(request.form['request_data'])

                ajax_handler.posted_file = image_file
                ajax_handler.posted_data = post_data

                response_data = ajax_handler.processRequest()

                if response_data:
                    return process_response(response_data)
                else:
                    return False
        else:
            # Bad POST request - No post data
            return False
    else:
        return render_template('catalog.html')


# Helper Functions

# Processes the response_data object handed back by the AjaxHandler
def process_response(response_data):
    response = []
    for template in response_data.templates:
        if template:
            response.append(render_template(template, categories=response_data.categories, items=response_data.items))

    return json.dumps(response)


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
