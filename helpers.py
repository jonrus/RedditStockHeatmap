import time

def readable_time(utc_time):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(utc_time))