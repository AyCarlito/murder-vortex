from flask import Flask, render_template, request, escape
from werkzeug.utils import redirect
from werkzeug.exceptions import BadRequest, TooManyRequests
from app import process
from apscheduler.schedulers.background import BackgroundScheduler
from time import time
import csv
import random
import atexit

app = Flask(__name__)

DENY_REQUEST_THRESHOLD = 1.5

connections = {}

BASE_URL = "https://en.wikipedia.org"
ALL_KILLERS_URL = "https://en.m.wikipedia.org/wiki/List_of_serial_killers_by_country"


def update_killer_list_and_purge():
    process.scrape_killer_list(ALL_KILLERS_URL, "mf-section-1", "identified")
    process.scrape_killer_list(ALL_KILLERS_URL, "mf-section-2", "unidentified")
    connections = {}

scheduler = BackgroundScheduler()
scheduler.add_job(func=update_killer_list_and_purge, trigger="interval", hours=24)
scheduler.start()
atexit.register(lambda: scheduler.shutdown())

def accept_or_deny_request(request):
    ip = request.remote_addr
    recieved_at = time()
    if ip in connections and (recieved_at - connections.get(ip)) < DENY_REQUEST_THRESHOLD:
        raise TooManyRequests("Please wait before requesting again")
    connections.update({ip: recieved_at})

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/killer", methods=["POST"])
def get_killer():
    accept_or_deny_request(request)
    killer_type = list(request.form.keys())[0]
    if killer_type not in ["identified", "unidentified"]:
         raise BadRequest("Request made must either be 'Identified' or 'Unidentified'")
    try:
        with open("data/%s_killers.csv" % killer_type, "r") as f:
            reader = csv.reader(f)
            killers = list(reader)
    except FileNotFoundError as e:
        update_killer_list_and_purge()
    return redirect(BASE_URL + random.choice(killers[0]))

if __name__ == "__main__":
    app.run()


