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

    def _timeframe_valueerror_txt(self) -> str:
        """
        Return the error text for self.app.timeframe having an invalid value
        """
        return f"CalendarRenderer.app.timeframe is not MONTH, WEEK, or DAY. Instead it is {self.app.timeframe}"

    def _calc_rows_needed(self) -> int:
        """
        Calculate the number of rows needed, by doing arithmetic with days for a month timeframe, or returning a static
        24 * 7 for a week or day timeframe.
        """
        now = datetime.datetime.now()
        if self.app.timeframe is calendarapp.Timeframe.MONTH:
            # calculate rows based on weeks
            # get weekday the month starts on
            monthrange = calendar.monthrange(now.year, now.month)
            # as calendar.monthrange returns weekday start, length of month
            # we can do this to calc how many cells are needed
            no_of_cells = sum(monthrange) - START_OF_WEEK
            return maths_helpers.ceildiv(no_of_cells, DAYS_IN_WEEK)
        elif self.app.timeframe in (calendarapp.Timeframe.WEEK, calendarapp.Timeframe.DAY):
            # one row per half hour
            # TODO remove magic numbers
            return 24 * 2
        else:
            raise ValueError(self._timeframe_valueerror_txt())

    def _get_columns_needed(self) -> int:
        """
        Get the number of columns needed, which is wholly and staticly dependent upon self.app.timeframe
        Each column represents a day
        """
        if self.app.timeframe in (calendarapp.Timeframe.MONTH, calendarapp.Timeframe.WEEK):
            return DAYS_IN_WEEK
        elif self.app.timeframe is calendarapp.Timeframe.DAY:
            # 1 column for 1 day
            return 1
        else:
            raise ValueError(self._timeframe_valueerror_txt())

    def render(self):
        return ""  # TODO
