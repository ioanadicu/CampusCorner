import flask

import calendarapp
import calendarrenderer

app = flask.Flask(__name__)

@app.route("/form", methods=("GET", "POST"))
def form():
    if flask.request.method == "POST":
        cal_link = flask.request.form["cal_link"]
        # here, put the calendar link into the db
        return flask.redirect(flask.url_for("calendar"))

    return flask.render_template("form.html")

@app.route("/calendar")
def calendar():
    calendar_app = calendarapp.CalendarApp()

    # read from db
    # for url in calendar_urls:
    #     calendar_app.add_calendar_from_url(url)

    renderer = calendarrenderer.CalendarRenderer(calendar_app)

    return renderer.render()
