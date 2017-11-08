"""Calendar utility"""

MONTH_NAME = ["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]
DAY_NAME = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
_31_DAYS_MONTHS = {1, 3, 5, 7, 8, 10, 12}
_30_DAYS_MONTHS = {4, 6, 9, 11}

def num_of_day(month, year):
    """Return number of days in month of year."""
    if month in _31_DAYS_MONTHS:
        return 31
    elif month in _30_DAYS_MONTHS:
        return 30
    elif month == 2:
        return 29 if year % 400 == 0 or (((year % 4) == 0) and ((year % 100) != 0)) else 28

def day_of_week(day, month, year):
    """Calculate day is which day of which of year."""
    bias = (14 - month) // 12
    m_year = year - bias
    mth = month + 12 * bias - 2
    return (day + m_year + m_year // 4 - m_year // 100 + m_year // 400 + (31 * mth) // 12) % 7

def calculate_date(month, year):
    """Calculate calendar.

    Return list of days in month."""
    start_index = day_of_week(1, month, year)
    end_index = num_of_day(month, year)
    padding_day = [0 for i in range(0, start_index)]
    days = [i for i in range(1, end_index + 1)]
    return padding_day + days

def align_day_block(day):
    """Return stylized day block for printing."""
    if day == 0:
        return "   "
    elif day > 0 and day < 10:
        return " " + str(day) + " "

    return " " + str(day)

def print_calendar(month, year):
    """Print calendar of a month of year."""
    print MONTH_NAME[month - 1] + ', ' + str(year)

    calendar = calculate_date(month, year)
    for i in DAY_NAME:
        print(i),

    print

    for i in range(len(calendar)):
        if calendar[i] == 0:
            print(align_day_block(0)),
        else:
            print(align_day_block(calendar[i])),

        if i % 7 == 0:
            print
