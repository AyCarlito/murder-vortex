from flask import Flask, render_template, request
from werkzeug.utils import redirect
from app import process
from apscheduler.schedulers.background import BackgroundScheduler
import csv
import random
import atexit

app = Flask(__name__)


BASE_URL = "https://en.wikipedia.org"
ALL_KILLERS_URL = "https://en.m.wikipedia.org/wiki/List_of_serial_killers_by_country"


def update_killer_list():
    process.scrape_killer_list(ALL_KILLERS_URL, "mf-section-1", "identified")
    process.scrape_killer_list(ALL_KILLERS_URL, "mf-section-2", "unidentified")

scheduler = BackgroundScheduler()
scheduler.add_job(func=update_killer_list, trigger="interval", hours=24)
scheduler.start()
atexit.register(lambda: scheduler.shutdown())

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/killer", methods=["POST"])
def get_killer():
    killer_type = list(request.form.keys())[0]
    with open("data/%s_killers.csv" % killer_type, "r") as f:
        reader = csv.reader(f)
        killers = list(reader)
    return redirect(BASE_URL + random.choice(killers[0]))

if __name__ == "__main__":
    app.run(debug=True)


