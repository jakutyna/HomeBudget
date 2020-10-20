import datetime
import pytest

from homebudget_app.functions.functions import month_first_last_day


@pytest.mark.parametrize("year, month, result", (
        (1995, 4, (datetime.date(1995, 4, 1), datetime.date(1995, 4, 30))),
        (2020, 8, (datetime.date(2020, 8, 1), datetime.date(2020, 8, 31))),
        (2022, 2, (datetime.date(2022, 2, 1), datetime.date(2022, 2, 28))),
        (2025, 12, (datetime.date(2025, 12, 1), datetime.date(2025, 12, 31))),
))
def test_month_first_last_day(year, month, result):
    assert month_first_last_day(year, month) == result
