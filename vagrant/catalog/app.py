import os
from flask import Flask, render_template, url_for, request, jsonify
from werkzeug.utils import secure_filename
from AjaxHandler import AjaxHandler
from ImageHelper import ImageHelper
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item
import json

UPLOAD_FOLDER = '/static/img'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# engine = create_engine('postgresql:///catalog')
engine = create_engine('mysql://andkim:andkim@localhost:3306/catalog', pool_recycle=3600)
Base.metadata.bind = engine

DBSessionMaker = sessionmaker(bind=engine)
dbSession = DBSessionMaker()
""":type: sqlalchemy.orm.Session"""

ajax_handler = AjaxHandler(dbSession)


@app.route("/")
@app.route("/catalog", methods=["GET", "POST"])
def catalog():
    if request.method == 'POST':
        post_data = request.get_json(silent=True, force=True)
        if post_data:
            # Normal ajax json post
            ajax_handler.posted_data = post_data
            response_data = ajax_handler.processRequest()  # ResponseData object
            if response_data:
                return process_response(response_data)
            else:
                return False
        else:
            #File included in request - first save the file in filesystem
            image_file = request.files['file_data']
            if image_file and is_image(image_file.filename):
                image_filename = secure_filename(image_file.filename)
                image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
            post_data = json.loads(request.form['request_data'])
            ajax_handler.posted_data = post_data
            response_data = ajax_handler.processRequest()
            # Handle uploaded files in ajax post
            image_helper = ImageHelper(request.files['file_data'])
            if image_helper.save_file():


            if response_data:
                return process_response(response_data)
            else:
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

def is_image(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
