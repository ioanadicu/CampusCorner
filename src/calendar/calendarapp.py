from enum import Enum
import typing
from pathlib import Path

import requests
import icalendar

class Timeframe(Enum):
    """
    Enum of potential timeframes the calendar app can display
    """
    DAY = 1
    WEEK = 2
    MONTH = 3

class CalendarApp:
    """
    Class representing an instance of the Calendar app. Should contain all necessary info to render the entire webpage
    with the frontend renderer.

    Attributes
    ==========
    `timeframe`: a `Timeframe` object of what timeframe is currently being displayed. Initialised to
        `Calendar.DEFAULT_TIMEFRAME`.
    `calendars`: `list` of `Calendar`s displayed on the web app
    """
    DEFAULT_TIMEFRAME = Timeframe.MONTH

    def __init__(self, calendars: typing.List[icalendar.Calendar]):
        self.timeframe = CalendarApp.DEFAULT_TIMEFRAME
        self.calendars = calendars

    def add_calendar_from_url(self, url: str):
        """
        Add a calendar from an .ics link

        :param url: `str` of the .ics link
        """
        request = requests.get(url)
        self.add_calendar(icalendar.Calendar.from_ical(request.text))

    def add_calendar_from_file(self, fp: str):
        """
        Add a calendar from a file

        :param fp: `str` of the filepath
        """
        ics_path = Path(fp)
        self.add_calendar(icalendar.Calendar.from_ical(ics_path.read_bytes()))

    def add_calendar(self, calendar: icalendar.Calendar):
        self.calendars.append(calendar)
