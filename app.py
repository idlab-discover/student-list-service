import os
import time
from dotenv import load_dotenv
from flask import Flask, after_this_request, request, jsonify, render_template, send_from_directory
from werkzeug.utils import secure_filename
from convert import ldap_convert, process_csv


app = Flask(__name__)
load_dotenv()


@app.route("/")
def index():
    return render_template("upload.html")


@app.post("/convert/csv")
def convert_csv():
    file = request.files["file"]

    if file:
        orig_filename = secure_filename(file.filename)
        new_filename = f"{orig_filename.split('.')[0]}_{str(time.time_ns() // 1_000_000)}.csv"
        save_path = os.path.join("uploads", new_filename)
        file.save(save_path)

        converted_csv_filename = process_csv(new_filename)

        @after_this_request
        def remove_files(response):
            try:
                os.remove(save_path)
                os.remove(os.path.join("outputs", converted_csv_filename))
            except Exception as err:
                print(f"Could not remove temp files: {err}")
                pass
            return response

        return send_from_directory("outputs", converted_csv_filename)
    else:
        return handle_error(400, "No csv file found.")


@app.post("/convert/json")
def convert_json():
    students = request.json["students"]

    if students is None:
        return handle_error(400, "No student list found in request body.")

    return ldap_convert(students)


def handle_error(code, message):
    return jsonify({"message": message, "code": code}), code
