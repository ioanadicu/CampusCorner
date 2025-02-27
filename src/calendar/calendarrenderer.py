import datetime
import calendar

import calendarapp
import maths_helpers

# monday is 0; sunday is 6
START_OF_WEEK = 0
DAYS_IN_WEEK = 7

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
            monthrange = calendar.monthrange(now.year, now.month)
            # as calendar.monthrange returns weekday start, length of month
            # we can do this to calc how many cells are needed
            no_of_cells = sum(monthrange) - START_OF_WEEK
            return maths_helpers.ceildiv(no_of_cells, DAYS_IN_WEEK)
        elif self.app.timeframe is calendarapp.Timeframe.WEEK:
            # one row per half hour
            # TODO remove magic numbers
            return 24 * 2
        elif self.app.timeframe is calendarapp.Timeframe.DAY:
            # TODO remove magic number
            return 24 * 2
        else:
            raise ValueError(f"CalendarRenderer.app.timeframe is not MONTH, WEEK, or DAY. Instead it is "
                             f"{self.app.timeframe}")

    def render(self):
        return ""  # TODO
