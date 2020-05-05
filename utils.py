from datetime import date, timedelta
import pandas as pd
from inspect import getfullargspec


def date_range(start, stop, skip=1):
    daycount = (stop - start).days
    for i in range(0, daycount, skip):
        yield start + timedelta(days=i)


def weekdays(start, stop, skip=1):
    return [d for d in date_range(start, stop, skip) if d.weekday() not in (5, 6)]


def split_dates_helper(start_date, end_date, interval_days = 365):
    final_date = end_date
    end_date = start_date + timedelta(days=interval_days)
    ret = []
    while start_date <= final_date:
        if end_date > final_date: end_date = final_date
        ret.append((start_date, end_date))
        start_date = end_date + timedelta(days = 1)
        end_date = start_date + timedelta(days = interval_days)
    return ret

def split_dates(func):
    '''Decorate func to run once per year and concatenate results.Func must have a start_date and end_date parameters, and return a tuple of DataFrames.'''
    def function_wrapper(*args, **kwargs):
        start_index = getfullargspec(func).args.index('start_date')
        end_index = getfullargspec(func).args.index('end_date')
        start_date_orig, end_date_orig = (args[start_index], args[end_index])
        dates = split_dates_helper(start_date_orig, end_date_orig, 180)
        results = []
        for start_date, end_date in dates:
            new_args = list(args)
            new_args[start_index] = start_date
            new_args[end_index] = end_date
            results.append(func(*new_args, **kwargs))
        if len(results) == 0: return results
        return  (pd.concat([row[i] for row in results]) for i in range(len(results[0])))
    return function_wrapper
