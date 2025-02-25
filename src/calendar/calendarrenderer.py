import datetime
import calendarapp

# monday is 0; sunday is 6
START_OF_WEEK = 0

class CalendarRenderer:
    """
    Class representing an instance of the calendar app which can render the CalendarApp as HTML. The .render() method
    returns HTML as a string.
    """

    def __init__(self, app: calendarapp.CalendarApp):
        self.app = app

    def _calc_rows_needed(self) -> int:
        now = datetime.datetime.now()
        if self.app.timeframe is calendarapp.Timeframe.MONTH:
            # calculate rows based on weeks
            # get weekday the month starts on
            month_starts_on = datetime.date(now.year, now.month, 1).weekday()
            # TODO

    def render(self):
        return ""  # TODO
