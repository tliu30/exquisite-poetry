from flask import url_for
from . import webapp

@webapp.route("/", methods=["GET"])
def home():
    return f'''
    <html>
        <body>
            Hello - <a href="{url_for("webapp.start_new_poem")}">start here!</a>
        </body>
    </html>'''
