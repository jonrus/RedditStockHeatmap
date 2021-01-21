import datetime

def readable_time(utc_time):
    """Returns given epoch time as a string"""
    # return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(utc_time))
    return str(datetime.datetime.fromtimestamp(utc_time))

def str_to_epoch(str_time):
    """
    Converts a string to epoch time
    Expects date in format;
    YYYY-mm-dd HH:mm:ss+tzoffset
    Example;
    '2021-01-01 12:00:00+0000'
    """
    return datetime.datetime.strptime(str_time, "%Y-%m-%d %H:%M:%S%z").timestamp()