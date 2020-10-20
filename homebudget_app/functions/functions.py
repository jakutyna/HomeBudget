import calendar, datetime


def month_first_last_day(year, month):
    """Returns dates of first and last days of given month.

    Args:
        year: Integer representing a year.
        month: Integer representing a number of month in a year.

    Returns:
        A tuple with dates of first and last days of a given month in a given year.
    """
    num_of_days = calendar.monthrange(year, month)[1]
    first_day = datetime.date(year, month, 1)
    last_day = first_day + datetime.timedelta(days=num_of_days - 1)
    return first_day, last_day
