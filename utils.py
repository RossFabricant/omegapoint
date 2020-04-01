from datetime import date, timedelta

def date_range(start, stop, skip=1):
    daycount = (stop - start).days
    for i in range(0, daycount, skip):
        yield start + timedelta(days=i)
        
def weekdays(start, stop, skip=1):
    return [d for d in date_range(start, stop, skip) if d.weekday() not in (5, 6)]
