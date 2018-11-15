import os
# import requests

from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from collections import Counter


UPLOAD_FOLDER = '../'
ALLOWED_EXTENSIONS = set(['txt', 'rst'])


def allowed_file(filename):
    return filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'python_parser.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # config upload folder
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # index route is file upload
    @app.route('/', methods=['GET', 'POST'])
    def upload_file():
        if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)

                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                file_url = url_for('upload_file', filename=filename)
                with open(filename) as f:
                    read_data = f.read()
                    word_freq = Counter(read_data.split()).most_common()
                    word_count = len(read_data.split())


        return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form method=post enctype=multipart/form-data>
          <input type=file name=file>
          <input type=submit value=Upload>
        </form>
        '''
    from flask import send_from_directory

    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    from . import db
    db.init_app(app)

    return app
