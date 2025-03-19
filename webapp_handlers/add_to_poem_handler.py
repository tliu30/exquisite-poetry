from . import webapp
from flask import render_template


@webapp.route("/addition/<poem_id>", methods=["GET", "POST"])
def add_to_poem(poem_id: str):
    return render_template(
        "add_to_poem.html",
        poem_id=poem_id,
    )
