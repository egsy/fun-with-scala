import os
from flask import Flask, flash, request, redirect, jsonify, url_for
from werkzeug.utils import secure_filename
from collections import Counter
from . import app


def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(["txt", "rst"])
    return filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# a simple page that says hello
@app.route("/hello")
def hello():
    return "Hello, World! This is a refactorrrrrrr."


# index route is file upload
@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        # check if the post request has the file part
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            file_parse = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file_url = url_for("upload_file", filename=filename)
            with open(file_parse) as f:
                read_data = f.read()
                word_freq = Counter(read_data.split()).most_common()
                word_count = len(read_data.split())
            return jsonify(count=word_count, freq=word_freq)

    return """
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    """


from flask import send_from_directory


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)
