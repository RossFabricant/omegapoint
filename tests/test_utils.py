"""Tests for the utils module."""
import pytest
from datetime import date, timedelta
import pandas as pd
from omegapoint import utils

def test_date_range():
    """Test the date_range function."""
    start = date(2022, 1, 1)
    stop = date(2022, 1, 10)
    dates = list(utils.date_range(start, stop))
    
    assert len(dates) == 10
    assert dates[0] == start
    assert dates[-1] == stop
    assert dates[5] == date(2022, 1, 6)

def test_date_range_with_skip():
    """Test the date_range function with a skip parameter."""
    start = date(2022, 1, 1)
    stop = date(2022, 1, 10)
    dates = list(utils.date_range(start, stop, skip=2))
    
    assert len(dates) == 5
    assert dates[0] == start
    assert dates[-1] == date(2022, 1, 9)
    assert dates[2] == date(2022, 1, 5)

def test_weekdays():
    """Test the weekdays function."""
    # Saturday to next Sunday
    start = date(2022, 1, 1)  # Saturday
    stop = date(2022, 1, 9)   # Sunday
    
    weekday_dates = utils.weekdays(start, stop)
    
    # Should only include Monday-Friday (Jan 3-7)
    assert len(weekday_dates) == 5
    assert weekday_dates[0] == date(2022, 1, 3)  # Monday
    assert weekday_dates[-1] == date(2022, 1, 7)  # Friday

def test_stepwise():
    """Test the stepwise function."""
    test_list = list(range(10))
    
    # Step size of 3
    steps = list(utils.stepwise(test_list, 3))
    assert len(steps) == 4
    assert steps[0] == [0, 1, 2]
    assert steps[1] == [3, 4, 5]
    assert steps[2] == [6, 7, 8]
    assert steps[3] == [9]
    
    # Step size larger than list
    steps = list(utils.stepwise(test_list, 20))
    assert len(steps) == 1
    assert steps[0] == test_list