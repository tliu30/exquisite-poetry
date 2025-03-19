from . import webapp

from flask import render_template


@webapp.route("/start/", methods=["GET", "POST"])
def start_new_poem():
    return render_template("start.html")
