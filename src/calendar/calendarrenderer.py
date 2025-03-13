import datetime
import calendar
import typing
import icalendar
import jinja2

import calendarapp
import maths_helpers

# monday is 0; sunday is 6
# note: if you want to change the start of the week or make it variable, you can't just replace this value;
# the start of the week being monday is hardcoded into some of the logic so read through carefully
# most of it is hopefully marked w todo but not necessarily
START_OF_WEEK = 0
DAYS_IN_WEEK = 7

class CalendarRenderer:
    """
    Class representing an instance of the calendar app which can render the CalendarApp as HTML. The .render() method
    returns HTML as a string.

    attributes
    ==========
    - `app` = a `CalendarApp` which can be rendered
    - `_now` = defaults to None and represents a faux-"now" as a quick hack to display other months/weeks/etc. Do not
               access or set directly—see below instead

    The `now` property
    ==================
    A CalendarRenderer has a property `.now` which represents a fixed point around which to display the calendar. By
    default, this calls `datetime.datetime.now()`, but you can set it to any datetime:
    ```py
    calendar_app.now = datetime.datetime(2022, 01, 01)
    ```
    To access this fixed point, also use `.now`. Generally, you should be using the `.now` property any time you would
    ordinarily call `datetime.datetime.now()`, and use `.now.date()` where you would normally call
    `datetime.date.today()`
    """

    def __init__(self, app: calendarapp.CalendarApp, *, now: datetime.datetime = None):
        self.app = app
        self._now = now

    @property
    def now(self):
        return self._now if self._now else datetime.datetime.now()

    @now.setter
    def now(self, value: datetime.datetime):
        self._now = value

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
        return maths_helpers.ceildiv(
            (self.get_end_date_of_display() - self.get_start_date_of_display()).days,
            DAYS_IN_WEEK
        )

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
        Return a datetime object representing the start of the time period displayed by the calendar
        """
        # TODO do for displays other than month
        today = self.now.date()
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

    def get_end_date_of_display(self) -> datetime.datetime:
        """
        Return a datetime object representing the end of the time period displayed on the calendar
        """
        # similar logic to start date, see above comments
        today = self.now.date()
        # we find the difference between the end of the month and the start of next week
        # eg weekday() gives us 3 (thursday)
        # we do 7 - 3 = 4 as there's 4 days difference between thurs and start of next week
        # fri sat sun mon
        # we want the start of next week as we'll pick midnight for the datetime
        # so in practice will only include the end of the week
        # todo don't hardcode week as starting with monday
        diff_from_end_of_week = DAYS_IN_WEEK \
                                - datetime.date(
            today.year,
            today.month,
            calendar.monthrange(today.year, today.month)[1]
        ).weekday()
        # first day of the first full week of next month
        upper_bound = datetime.date(
            today.year,
            today.month,
            calendar.monthrange(today.year, today.month)[1]
        ) \
            + datetime.timedelta(days=diff_from_end_of_week)
        # date -> datetime
        return datetime.datetime(upper_bound.year, upper_bound.month, upper_bound.day)
    
    def _get_displayed_events(self) -> typing.List[icalendar.Event]:
        events = []
        for cal in self.app.calendars:
            # list of icalendar Events
            for event in cal.events:
                # NOTE: naive datetime instances will be assumed to represent local time
                # get_start_date_of_display() will be naive whilst DTEND and DTSTART will have timezones
                # TODO: possibly attempt to convert start date to same timezone as DTEND/DTSTART
                if (self.get_start_date_of_display().timestamp() <= event.DTEND.timestamp()) \
                            and(event.DTSTART.timestamp() < self.get_end_date_of_display().timestamp()):
                    events.append(event)

        return events

    def render_table(self) -> str:
        """
        Return a string of the Calendar table
        """
        # a string that goes between <table></table> tags
        rows = ""

        # add header
        if self.app.timeframe in (calendarapp.Timeframe.MONTH, calendarapp.Timeframe.WEEK):
            rows += """<tr class="calrow">
    <th>Mon</th>
    <th>Tue</th>
    <th>Wed</th>
    <th>Thu</th>
    <th>Fri</th>
    <th>Sat</th>
    <th>Sun</th>
</tr>"""
        elif self.app.timeframe is calendarapp.Timeframe.DAY:
            rows += f"<tr class=\"calrow\"><th>{self.now.day}</th></tr>"

        for row in range(self._calc_rows_needed()):
            # a string that goes betweem <tr></tr> tags
            cells = ""
            for column in range(self._get_columns_needed()):
                # days into the displayed timeframe
                days_in = row * DAYS_IN_WEEK + column
                start_of_day = self.get_start_date_of_display() + datetime.timedelta(days=days_in)
                start_of_next_day = start_of_day + datetime.timedelta(days=1)

                todays_events = []
                for event in self._get_displayed_events():
                    # see comment re: naive datetimes under _get_displayed_events()
                    if (start_of_day.timestamp() <= event.DTEND.timestamp()) \
                        and (start_of_next_day.timestamp() > event.DTSTART.timestamp()):
                        todays_events.append(event)

                cell_string = ""
                cell_string += '<div class="caldate">' + str(start_of_day.day) + '</div>'

                for event in todays_events:
                    cell_string += '<div class="calevent">' + event["summary"] + '</div>'

                cells += '<td class="calcell">' + cell_string + '</td>'

            rows += '<tr class="calrow">' + cells + '</tr>'

        return '<table class="caltable">' + rows + '</table>'

    def render(self):
        env = jinja2.Environment(loader = jinja2.FileSystemLoader('templates'))
        template = env.get_template('calendar.html')
        return template.render(calendar_table = self.render_table())
