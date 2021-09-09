from flask import Flask, render_template, request
from werkzeug.utils import redirect
from app import process
import schedule
import time
import csv
import random

app = Flask(__name__)


BASE_URL = "https://en.wikipedia.org"
ALL_KILLERS_URL = "https://en.m.wikipedia.org/wiki/List_of_serial_killers_by_country"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/killer", methods=["POST"])
def killer():
    killer_type = list(request.form.keys())[0]
    with open("data/%s_killers.csv" % killer_type, "r") as f:
        reader = csv.reader(f)
        killers = list(reader)
    return redirect(BASE_URL + random.choice(killers[0]))

if __name__ == "__main__":
    app.run(debug=True)


