import datetime
import calendar
import typing
import icalendar

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

    def get_start_date_of_display(self) -> datetime.datetime:
        """
        Returns a 2-tuple of the start of the range of dates shown by the calendar, and the end of the range of dates
        shown by the calendar.
        """
        # TODO do for displays other than month
        today = datetime.date.today()
        # gets the weekday that the 1st of the month starts on
        # which is also a diff from the start of the week
        # monday = 0
        # eg if below returns 3 then it's thurs and 3 day difference from week start
        diff_from_start_of_week = datetime.date(today.year, today.month, 1).weekday()
        # so we can get the start of the range by
        start_of_range = datetime.date(today.year, today.month, 1) \
                         - datetime.timedelta(days=diff_from_start_of_week)
        # return datetime object of the start of range (which is currently just a date object)
        return datetime.datetime(start_of_range.year, start_of_range.month, start_of_range.day)
    
    def _get_months_events(self) -> typing.List[icalendar.Event]:
        events = []
        for cal in self.app.calendars:
            # list of icalendar Events
            for event in cal.events:
                pass
            # TODO

    def render_table(self) -> str:
        """
        Return a string of the Calendar table
        """
        # a string that goes between <table></table> tags
        rows = ""

        # add header
        if self.app.timeframe in (calendarapp.Timeframe.MONTH, calendarapp.Timeframe.WEEK):
            rows += """<tr>
    <th>Mon</th>
    <th>Tue</th>
    <th>Wed</th>
    <th>Thu</th>
    <th>Fri</th>
    <th>Sat</th>
    <th>Sun</th>
</tr>"""
        elif self.app.timeframe is calendarapp.Timeframe.DAY:
            rows += f"<tr><th>{datetime.datetime.now().day}</th></tr>"

        for row in range(self._calc_rows_needed()):
            # a string that goes betweem <tr></tr> tags
            cells = ""
            for column in range(self._get_columns_needed()):
                pass

    def render(self):
        return ""  # TODO
