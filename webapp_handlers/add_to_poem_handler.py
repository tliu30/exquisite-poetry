from . import webapp
from flask import request
from flask import render_template
from logic import poem_logic
from logic import email_logic
from flask import abort
from wtforms import Form
from wtforms import StringField
from wtforms import TextAreaField
from wtforms import validators


class NewSegmentForm(Form):
    your_email = StringField(
        "Your Email",
        [validators.DataRequired()],
    )
    next_email = StringField(
        "Next Writer Email",
        [],
    )
    text = TextAreaField("Poem", [validators.DataRequired()])


@webapp.route("/segment/<segment_uid>", methods=["GET", "POST"])
def segment(segment_uid: str):
    segment = poem_logic.get_segment(segment_uid)

    if not segment:
        return abort(404)

    previous_segment = poem_logic.get_segment(segment.previous_segment_uid)
    hint = ""
    if previous_segment:
        hint = previous_segment.text.split("\n")[-1]

    is_last_segment = poem_logic.is_the_poem_full(segment.poem_uid)

    form = NewSegmentForm(request.form)

    extra_validators = {}
    if not is_last_segment:
        extra_validators["next_email"] = [validators.DataRequired()]

    if request.method == "POST" and form.validate(extra_validators=extra_validators):
        poem_logic.update_segment(segment, form.text.data)
        email_logic.send_email_to_writer(segment.uid, form.your_email.data)

        if not is_last_segment:
            next_segment = poem_logic.create_next_segment(segment)
            email_logic.send_email_to_next(next_segment.uid, form.next_email.data)

    if segment.incomplete:
        return render_template(
            "segment_incomplete.html",
            hint=hint,
            form=form,
            is_last_segment=is_last_segment,
        )
    else:
        if poem_logic.is_poem_done(segment.poem_uid):
            complete_segments = [
                record.text for record in poem_logic.get_all_segments(segment.poem_uid)
            ]
            return render_template(
                "segment_poem_complete.html",
                text="\n\n".join(complete_segments),
            )
        else:
            return render_template(
                "segment_complete.html",
                hint=hint,
                text=segment.text,
            )
