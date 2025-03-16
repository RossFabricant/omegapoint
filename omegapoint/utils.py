from datetime import date, timedelta
import pandas as pd
from inspect import getfullargspec
from typing import Generator, List, Tuple, Any, Callable, Iterator, TypeVar, cast

T = TypeVar('T')

def date_range(start: date, stop: date, skip: int = 1) -> Generator[date, None, None]:
    """Generate a range of dates from start to stop with a given skip interval.
    
    Args:
        start: The start date (inclusive)
        stop: The end date (inclusive)
        skip: Number of days to skip between dates (default: 1)
        
    Yields:
        date: Each date in the range
    """
    daycount = (stop - start).days
    for i in range(0, daycount+1, skip):
        yield start + timedelta(days=i)


def weekdays(start: date, stop: date, skip: int = 1) -> List[date]:
    """Filter a date range to include only weekdays (Monday-Friday).
    
    Args:
        start: The start date
        stop: The end date
        skip: Number of days to skip between dates (default: 1)
        
    Returns:
        List[date]: Filtered list of weekdays between start and stop
    """
    return [d for d in date_range(start, stop, skip) if d.weekday() not in (5, 6)]


def split_dates_helper(start_date: date, end_date: date, interval_days: int = 365) -> List[Tuple[date, date]]:
    """Split a date range into chunks of a specified interval.
    
    Args:
        start_date: The start date
        end_date: The end date
        interval_days: Maximum number of days per chunk (default: 365)
        
    Returns:
        List[Tuple[date, date]]: List of (start_date, end_date) tuples for each chunk
    """
    final_date = end_date
    end_date = start_date + timedelta(days=interval_days)
    ret = []
    while start_date <= final_date:
        if end_date > final_date:
            end_date = final_date
        ret.append((start_date, end_date))
        start_date = end_date + timedelta(days=1)
        end_date = start_date + timedelta(days=interval_days)
    return ret


def split_dates(func: Callable) -> Callable:
    """Decorate a function to run once per 180 days and concatenate results.
    
    The decorated function must have start_date and end_date parameters,
    and return a tuple of DataFrames. This is useful for API calls that
    can only handle a limited date range at once.
    
    Args:
        func: The function to decorate
        
    Returns:
        Callable: The decorated function that handles date splitting internally
    """
    def function_wrapper(*args: Any, **kwargs: Any) -> Iterator[pd.DataFrame]:
        start_index = getfullargspec(func).args.index("start_date")
        end_index = getfullargspec(func).args.index("end_date")
        start_date_orig, end_date_orig = (args[start_index], args[end_index])
        dates = split_dates_helper(start_date_orig, end_date_orig, 180)
        results = []
        for start_date, end_date in dates:
            new_args = list(args)
            new_args[start_index] = start_date
            new_args[end_index] = end_date
            results.append(func(*new_args, **kwargs))
        if len(results) == 0:
            return results
        return (pd.concat([row[i] for row in results]) for i in range(len(results[0])))

    return function_wrapper


def split_dates_df(func: Callable) -> Callable:
    """Decorate a function to run once per 180 days and concatenate results.
    
    The decorated function must have start_date and end_date parameters,
    and return a single DataFrame. This is useful for API calls that
    can only handle a limited date range at once.
    
    Args:
        func: The function to decorate
        
    Returns:
        Callable: The decorated function that handles date splitting internally
    """
    def function_wrapper(*args: Any, **kwargs: Any) -> pd.DataFrame:
        start_index = getfullargspec(func).args.index("start_date")
        end_index = getfullargspec(func).args.index("end_date")
        start_date_orig, end_date_orig = (args[start_index], args[end_index])
        dates = split_dates_helper(start_date_orig, end_date_orig, 180)
        results = []
        for start_date, end_date in dates:
            new_args = list(args)
            new_args[start_index] = start_date
            new_args[end_index] = end_date
            results.append(func(*new_args, **kwargs))
        if len(results) == 0:
            return results
        return pd.concat(results)

    return function_wrapper


def stepwise(lst: List[T], step: int) -> Generator[List[T], None, None]:
    """Step through a list in sections of specified size.
    
    This generator yields chunks of the list with a maximum size of 'step'.
    Useful for processing large lists in batches.
    
    Args:
        lst: The input list to divide into chunks
        step: The maximum size of each chunk
        
    Yields:
        List[T]: Chunks of the original list
    """
    if step > len(lst):
        yield lst
        return
        
    i = 0
    for i in range((len(lst) // step)):
        yield (lst[i * step : (i + 1) * step])
    
    l = lst[(i + 1) * step :]
    if len(l) > 0:
        yield l
