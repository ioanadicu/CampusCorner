from calendarapp import CalendarApp

class CalendarRenderer:
    """
    Class representing an instance of the calendar app which can render the CalendarApp as HTML. The .render() method
    returns HTML as a string.
    """

    def __init__(self, app: CalendarApp):
        self.app = app

    def render(self):
        return ""  # TODO
