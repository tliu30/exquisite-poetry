from . import webapp

from flask import render_template
from flask import request
from flask import url_for
from flask import redirect
from wtforms import Form
from wtforms import StringField
from wtforms import TextAreaField
from wtforms import IntegerField
from wtforms import validators
from logic import poem_logic
from logic import email_logic


class NewPoemForm(Form):
    your_email = StringField(
        "Your Email",
        [validators.DataRequired()],
    )
    next_email = StringField(
        "Next Writer Email",
        [validators.DataRequired()],
    )
    text = TextAreaField("Poem", [validators.DataRequired()])
    num_segments = IntegerField(
        "Number of Segments",
        [
            validators.DataRequired(),
            validators.NumberRange(min=3, max=10),
        ],
    )


@webapp.route("/start/", methods=["GET", "POST"])
def start_new_poem():
    form = NewPoemForm(request.form)
    if request.method == "POST" and form.validate():
        cur_segment = poem_logic.create_new_poem(
            form.text.data,
            form.num_segments.data,
        )
        next_segment = poem_logic.create_next_segment(cur_segment)
        email_logic.send_email_to_writer(cur_segment.uid, form.your_email.data)
        email_logic.send_email_to_next(next_segment.uid, form.next_email.data)

        return redirect(url_for("webapp.segment", segment_uid=cur_segment.uid))
    return render_template("start.html", form=form)
