

def convert_dates_to_datetime(obj):
    """Recursively convert date objects to datetime objects for MongoDB compatibility."""
    if isinstance(obj, dict):
        return {k: convert_dates_to_datetime(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [convert_dates_to_datetime(item) for item in obj]
    elif isinstance(obj, date) and not isinstance(obj, datetime):
        return datetime.combine(obj, datetime.min.time())
    return obj