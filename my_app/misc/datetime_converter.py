from my_app.apis import geo_locator_api
from my_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re  # the regex module
from my_app import app
from my_app.models import user as usr
from datetime import datetime
import time


class DateTime_Converter:
    def __init__(self):
        pass

    def get_current_unix_time(self):
        return int(time.time())

    def format_unix_time(self, unix_time):
        formatted_time = datetime.utcfromtimestamp(
            unix_time).strftime('%Y-%m-%d %H:%M:%S')
        return formatted_time

    def unix_to_datetimeObj(self, dt_unix):
        dt = datetime.fromtimestamp(int(dt_unix))
        return dt

    def datetimeObj_to_unix(self, dtObj):
        unix = time.mktime(dtObj.timetuple())
        # print(unix)
        return unix

    def get_datetime_formatted_from_dt_obj(self, dt=None):
        if not dt:
            dt = datetime.now()
        # time = self.format_time(dt)
        _time = dt.strftime("%I:%M%p")
        if _time[0] == "0":
            _time = _time[1:]
        # day, date = self.format_date(dt)
        date = dt.strftime("%B %d, %Y")
        day = dt.strftime("%A")
        return (day, date, _time)

    def get_datetime_formatted_from_unix(self, dt_unix):
        dt = datetime.fromtimestamp(int(dt_unix))
        day, date, _time = self.get_datetime_formatted_from_dt_obj(dt)
        return day, date, _time

    def convert_unix_to_24hr_min_sec(self, dt_unix):
        dt_object = datetime.utcfromtimestamp(dt_unix)
        time_list = dt_object.strftime("%H:%M:%S").split(":")
        hours, minutes, seconds = time_list
        #print('TIME: ', time_list)
        return hours, minutes, seconds

    def is_daytime_from_unix(self, dt_unix=None, zone_offset=None):
        if not dt_unix:
            dt_unix = int(time.time())
        if not zone_offset:
            # zone_offset = -32400
            zone_offset = -14400
            temp_time = dt_unix + zone_offset
            #print(f'Offset: {zone_offset}, dt_unix: {dt_unix}, temp_time: {temp_time}')
            dt_unix = temp_time
        _24hr, _, _ = self.convert_unix_to_24hr_min_sec(dt_unix)
        #print('(2) 24 HOUR: ', _24hr)
        if (int(_24hr) >= 6) and (int(_24hr) <= 20):
            # DAY TIME
            #print("Day Time")
            return True
        #print("Night Time")
        return False

    def current_loc_unix_timezone_offset_converter(self, dt_unix, timezone_offset):
        loc_time = dt_unix+timezone_offset
        day, date, time = self.get_datetime_formatted_from_unix(loc_time)
        return day, date, time
