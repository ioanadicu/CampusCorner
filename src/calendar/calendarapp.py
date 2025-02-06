from enum import Enum

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

    def __init__(self):
        self.timeframe = CalendarApp.DEFAULT_TIMEFRAME

