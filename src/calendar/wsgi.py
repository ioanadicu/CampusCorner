from flask import Flask
import yaml

import calendarapp
import calendarrenderer

CONFIG_PATH = "cal_testing_config.yaml"

app = Flask(__name__)

@app.route("/")
def main():
    # initialise app w/ no calendars yet
    calendar_app = calendarapp.CalendarApp()

    # add a calendar from url from config file
    config_file = open(CONFIG_PATH, "r")
    config = yaml.safe_load(config_file)
    calendar_app.add_calendar_from_url(config["cal_url"])

    # create renderer
    renderer = calenderrenderer.CalendarRenderer(calendar_app)

    return renderer.render()
