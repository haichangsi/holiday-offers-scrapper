from datetime import date, timedelta
import random

gen_period_start = date(2023, 5, 10)
gen_period_end = date(2023, 8, 10)


def date_range(start, end):
    for n in range(int((end - start).days) + 1):
        yield start + timedelta(n)


def rand_day_from_period(start=gen_period_start, end=gen_period_end):
    all_dates = list(date_range(start, end))
    return random.sample(all_dates, 1)


# move a list of lists of dates here? TBD
