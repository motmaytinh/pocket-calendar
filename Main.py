import datetime
import CalendarUtils as cal

now = datetime.datetime.now()

cal.print_calendar(now.month, now.year)
