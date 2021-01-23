"""Helper functions for the Reddit Stock Heatmap project"""
import datetime

def readable_time(utc_time):
    """Returns given UTC epoch time as a string"""
    return str(datetime.datetime.utcfromtimestamp(utc_time))

def str_to_epoch(str_time, add_utc_tz = False):
    """
    Converts a string to epoch time
    Expects date in format;
    YYYY-mm-dd HH:mm:ss+tzoffset - if add_utc_tz = False
    YYYY-mm-dd HH:mm:ss - if add_utc_tz = True
    add_utc_tz = False by default
    Example;
    str_to_epoch('2021-01-01 12:00:00+0000') -> 1609502400.0
    str_to_epoch('2021-01-01 12:00:00+0600') -> 1609480800.0
    str_to_epoch('2021-01-01 12:00:00', add_utc_tz = True) -> 1609502400.0
    You can pass it a UTC time with no time zone info and it will be auto added;
    Example;
    '2021-01-01 12:00:00' will be convert to '2021-01-01 12:00:00+0000'
    """
    if add_utc_tz:
        str_time += "+0000"
    
    return datetime.datetime.strptime(str_time, "%Y-%m-%d %H:%M:%S%z").timestamp()