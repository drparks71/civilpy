"""
CivilPy
Copyright (C) 2019 - Dane Parks

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
import json
from pathlib import Path

from flask import (
    Flask,
    render_template,
    render_template_string,
    request,
    jsonify,
    redirect,
    url_for,
)
from flask_dropzone import Dropzone
from json2html import *

# Library specific imports
from website.pdf_processing import get_data_from_pdf
import shutil

import folium

from website.mapping import m

# Added Comment to test ability to commit

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, template_folder="website/templates")

app.config.update(
    UPLOADED_PATH=os.path.join(basedir, "uploads"),
    # Flask-Dropzone config:
    DROPZONE_ALLOWED_FILE_TYPE="default",
    DROPZONE_MAX_FILE_SIZE=3,
    DROPZONE_MAX_FILES=30,
)

dropzone = Dropzone(app)


@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html", content="Testing Homepage")


@app.route("/data")
def data():
    """
    Creates an API endpoint for the application to pull the results of the python functions
    from a file. Only attempts to run once the users uploads a file into the "uploads" folder.
    """

    result_files = os.listdir(f"src/civilpy/flask/results/")
    uploads_files = os.listdir(f"src/civilpy/flask/uploads/")

    response = "Waiting on a file to process"

    for upload in uploads_files:
        if upload not in result_files:
            path_object = Path(upload)

            # Tell the application what to do with the file based on filetype
            # //TODO - Replace this with user interface controls like dropdown menus to cater the responses
            if path_object.suffix.lower() == ".pdf":
                get_data_from_pdf(
                    (os.getcwd() / "src/civilpy/flask/uploads" / path_object)
                )
            elif path_object.suffix.lower() == ".json":
                path_source = Path(os.getcwd(), "src/civilpy/flask/uploads", upload)
                path_dest = Path(os.getcwd(), "src/civilpy/flask/results", upload)
                shutil.copy(path_source, path_dest)
        else:
            if upload == ".gitkeep":  # Ignore the gitkeep file
                continue
            else:
                with open(f"src/civilpy/flask/results/{upload}", "r") as f:
                    response = json2html.convert(json=json.load(f))

                    return response

    return response


@app.route("/admin")
def admin():
    return redirect(url_for(user="Admin"))


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        f = request.files.get("file")
        file_path = os.path.join(app.config["UPLOADED_PATH"], f.filename)

        # Make sure the folder exists, create it if it doesn't
        if os.path.isdir(Path(file_path).parent):
            pass
        else:
            os.mkdir(Path(file_path).parent)
            os.mkdir(Path(file_path).parent.parent.parent / "results")

        f.save(file_path)
        response = "File Successfully Uploaded"

        return jsonify(data=response)
    return render_template("dropzone.html", content="Testing File Upload")


@app.route("/calculations")
def calculations():
    return render_template("index.html", content="Testing Calculations")


@app.route("/maps")
def maps():
    """Simple example of a fullscreen map."""
    return m.get_root().render()


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["nm"]
        return redirect(url_for(user=user))
    else:
        return render_template("login.html")


@app.route("/signup", methods=["POST", "GET"])
def signup():
    return render_template("sign_up.html", content="Signup Page")


@app.route("/logout")
def logout():
    return render_template("index.html", content="Logout Page")


if __name__ == "__main__":
    app.run(debug=True, port=8080)
