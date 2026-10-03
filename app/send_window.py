"""Beijing-time sending window, independent of the runner's system timezone."""
from datetime import datetime, timedelta, timezone
import random

BEIJING = timezone(timedelta(hours=8))

def now():
    return datetime.now(BEIJING)

def bounds(moment):
    local = moment.astimezone(BEIJING)
    return (local.replace(hour=11, minute=40, second=0, microsecond=0),
            local.replace(hour=12, minute=0, second=0, microsecond=0))

def allowed(moment):
    start, end = bounds(moment)
    return start <= moment.astimezone(BEIJING) < end

def choose_start(moment, randint=random.randint):
    start, end = bounds(moment)
    earliest = max(start, moment.astimezone(BEIJING))
    if earliest >= end:
        return None
    available = int((end - earliest).total_seconds())
    if available < 1:
        return None
    return earliest + timedelta(seconds=randint(0, available - 1))
