from flask import Flask
import configparser

import calendarapp
import calendarrenderer

CONFIG_PATH = "cal_testing_config.ini"

"""
At the path specified by CONFIG_PATH, the WSGI expects an INI formatted as

    [Settings]
    calURL = https://an.ics.url.here/calendar.ics
"""

app = Flask(__name__)

@app.route("/")
def main():
    # initialise app w/ no calendars yet
    calendar_app = calendarapp.CalendarApp()

    # add a calendar from url from config file
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    calendar_app.add_calendar_from_url(str(config["Settings"]["calURL"]))

    # create renderer
    renderer = calendarrenderer.CalendarRenderer(calendar_app)

    return renderer.render()

app.run(debug=True)
