from flask import Flask
import os
from flask import Flask, flash, request, redirect, jsonify, url_for
from werkzeug.utils import secure_filename
from collections import Counter
from . import db

UPLOAD_FOLDER = "../"
# config upload folder

# app = Flask(__name__)
app = Flask(__name__, instance_relative_config=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

import python_parser.views
import python_parser.db


def create_app(test_config=None):

    # create and configure the app
    # app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "python_parser.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    return app
