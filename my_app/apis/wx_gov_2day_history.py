import requests
from bs4 import BeautifulSoup as BS
import  time
import re
from my_app.apis.city_state_station_code import get_station_code_from_city_state
from my_app.error_logging import logger
from datetime import datetime, timedelta
#	result2 = (air2, wind2, pressure2, precip2, wx2)

class No_Wx_Data:
	def __init__(self, prev_day_date):
		self.temp_min = ""
		self.temp_max = ""

		self.wind_min = ""
		self.wind_max = ""
		self.wind_max_gust = ""

		self.pressure_min_time = ""
		self.pressure_max_time = ""
		self.pressure_min = ""
		self.pressure_max = ""

		self.precipitation = ""
		self.conditions = ""
		self.prev_day_date = prev_day_date


class Wx_Data:
	def __init__(self, temperature, wind, pressure, precipitation, conditions, prev_day_date):
		self.temp_min = temperature[0]
		self.temp_max = temperature[1]

		self.wind_min = wind[0]
		self.wind_max = wind[1]
		self.wind_max_gust = wind[2]

		self.pressure_min_time = pressure[0][0]
		self.pressure_max_time = pressure[1][0]
		self.pressure_min = pressure[0][1]
		self.pressure_max = pressure[1][1]

		self.precipitation = precipitation
		self.conditions = conditions
		self.prev_day_date = prev_day_date

	
def get_2day_history_dates():
	current_datetime = datetime.now()
	previous_datetime1 = current_datetime - timedelta(hours=24)
	previous_datetime2 = current_datetime - timedelta(hours=48)
	yesterday = previous_datetime1.strftime("%A %B %d, %Y")
	day_before_yesterday = previous_datetime2.strftime("%A %B %d, %Y")
	return (yesterday, day_before_yesterday)


def get_2day_history_data(city_state):
	city_code = get_station_code_from_city_state(city_state)
	print("City Code: ", city_code)
#	city_code = "KASH"
	url = f"https://w1.weather.gov/data/obhistory/{city_code}.html"
	
	res = requests.get(url)
	if res.status_code != 200:
		return
		
	page = BS(res.content, "html.parser" )
	rows = page.find_all("tr")
	col_names = []
	all_data = []
	for i, row in enumerate(rows):
		if i == 4:
			col_html = row.find_all("th")
			for j, name in enumerate(col_html):
	#			print(f"COL NUM: {j+1}")
				col_names.append(name.text)

		if i >= 7 and i <= 78:
			row_data = row.find_all("td")
			temp = []
			for j, row_item in enumerate(row_data):
				temp.append(row_item.text)
			all_data.append(temp)
# Determine past 2 full days	
	day = all_data[0][0]
	full_days = {}
	full_days[day] = 0
	for i, row in enumerate(all_data):
		if not row:
			continue
		this_day = row[0]
		if this_day not in full_days:
			full_days[this_day] = 1
		else:
			full_days[this_day] += 1
	
	days = full_days.keys()
	items = full_days.items()
	days_to_keep = []
	for day in days:
		if full_days[day] == 24:
			days_to_keep.append(day)

	final_data = []
	for i, row in enumerate(all_data):
		if not row:
			continue
		if row[0] in days_to_keep:
			final_data.append(row)
	return final_data, days


def is_number_regex(num):
	regex_num1 = "^-?\d*(\.\d+)?$"
	regex_num2 = "^-?(\.\d+)$"
	regex_num3 = "^-?\d+\."
	res1 = re.match(regex_num1, num)
	res2 = re.match(regex_num2, num)
	res3 = re.match(regex_num3, num)
	if res1 or res2 or res3:
		return True
	return False


def get_clean_string(the_string):
	if the_string == "":
		return
	cleaned_string = ""
	specials= ["\n", "\r", "\t", "\\"]
	white_space_counter = 0
	for index, char in enumerate(the_string):
		if char != " " and char not in specials:
			white_space_counter = 0
			cleaned_string +=  char
		if (char == " ") and (white_space_counter == 0) and (index != len(the_string)-1) and (len(cleaned_string) != 0):
			white_space_counter += 1
			cleaned_string += char
	if cleaned_string[-1] == " ":
		cleaned_string = cleaned_string[:-1]
	return cleaned_string


def split_day_data_2lists(data):
	day1 = []
	day2 = []
	day = data[0][0]
	for i, row in enumerate(data):
		if row[0] == day:
			day1.append(row)
		else:
			day2.append(row)
	return day1, day2


def parse_time(data):
	res = data.split(":")
	hour = int(res[0])
	minutes = int(res[1])
	if hour == 0:
		hour = 12
		result = f"{str(hour)}:{minutes}am"
		return result
	if hour == 12:
		result = f"{str(hour)}:{minutes}pm"
		return result
	if hour > 12:
		result = f"{str(hour-12)}:{minutes}pm"
		return result
	if hour < 12:
		result = f"{str(hour)}:{minutes}am"
		return result
	return
	

def find_max_occurance_of_str(dict):
	if not dict:
		print("No dict!")
	keys = list(dict.keys())
	max_ = -99999
	result = {}
	for key in keys:
		if key != "wind_speed":
			if dict[key] > max_:
				max_ = dict[key]
				result[key] = max_
	
	if not result:
		return
	
	final = []
	max_ = -99999
	max_indx = -1
	keys = list(result.keys())
	vals = list(result.values())
	for i, val in enumerate(vals):
		if val > max_:
			max_ = val
			max_indx = i
	final.append(keys[max_indx])
	return final
		

def get_average(data):
	if not data:
		return
	total = 0
	for i in data:
		if "." not in i:
			total += int(i)
		if "." in i:
			total += float(i)
	round_avg = round(total/len(data))
	avg = round(total/len(data),2)
	return round_avg, avg


def parse_wind(data):
	max_speed = ["", 0]
	min_speed = ["", 400]
	max_gust = ["", 0]

	for row in data:
		if not row[2]:
			continue
		wind = row[2].split(" ")
		wind_direction = ""

		if len(wind) == 2:
			wind_direction = wind[0]
			wind_speed = int(wind[1])
			
			if wind_speed > max_speed[1]:
				max_speed[1] = wind_speed
				max_speed[0] = wind_direction
				
			if wind_speed < min_speed[1]:
				min_speed[1] = wind_speed
				min_speed[0] = wind_direction
						
		if len(wind) == 4:
			wind_direction = wind[0]
			gust = int(wind[3])
			if gust > max_gust[1]:
				max_gust[1] = gust
				max_gust[0] = wind_direction
				
	if min_speed == 400 and max_speed == 0 and max_gust == 0:
		return 0, 0, 0
		
	min_speed[1] = str(min_speed[1])
	max_speed[1] = str(max_speed[1])
	max_gust[1] = str(max_gust[1])
	res_min = ' '.join(min_speed)
	res_max = ' '.join(max_speed)
	res_gust = ' '.join(max_gust)
	
	print(f"Wind Data: {res_min}, {res_max}, {res_gust}")
	return res_min, res_max, res_gust
			
			
def parse_weather_state(data):
	dict = {}
	for i, row in enumerate(data):
		wx = row[4]
		if wx not in dict:
			dict[wx] = 1
		if wx in dict:
			dict[wx] += 1
	if dict:
		res = find_max_occurance_of_str(dict)[0]
		return res
	return


def get_temp_min_max(data):
	min_ = 99999
	max_ = -99999
	for row in data:
		if row[6] != "NA":
			temp = int(row[6])
			if temp > max_:
				max_ = temp
			if temp < min_:
				min_ = temp
	return min_ ,  max_


def get_min_max_pressure(data):
	min_pressure = ['', 9999.9]
	max_pressure = ['', -9999.9]
	
	for i, row in enumerate(data):
		this_time = parse_time(row[1])
		pressure = float(row[13])
		
		if pressure > max_pressure[1]:
			max_pressure = [this_time, pressure]
		if pressure < min_pressure[1]:
			min_pressure = [this_time, pressure]
			

	if max_pressure[1] != -9999 and min_pressure[1] != 9999:

		min_pressure[1] = str(min_pressure[1])
		max_pressure[1] = str(max_pressure[1])
#		print(f"Min_Pressure: {min_pressure},\nMax_Pressure: {max_pressure}")
		return min_pressure, max_pressure
	return "NA", "NA"


def get_precipitation(data):
	# time range 6 - 20
	precip = 0
	for row in data:
#		this_time = parse_time(row[1])
#		if int(this_time) > 6 and int(this_time) < 20:
		temp = row[15]
		if temp:
			precip += float(temp)
	print(f"PRECIP: {precip}")
	return round(precip, 2)


def get_2day_weather_history(city_state):
	raw_data = get_2day_history_data(city_state)[0]
	
	day1, day2 = split_day_data_2lists(raw_data)
	day1_date, day2_date = get_2day_history_dates()

	wind1 = parse_wind(day1)
	wind2 = parse_wind(day2)

	wx1 = parse_weather_state(day1)
	wx2 = parse_weather_state(day2)

	air1_min, air1_max = get_temp_min_max(day1)
	air2_min, air2_max = get_temp_min_max(day2)

	pressure1_min, pressure1_max = get_min_max_pressure(day1)
	pressure2_min, pressure2_max = get_min_max_pressure(day2)

	precip1 = get_precipitation(day1)
	precip2 =	get_precipitation(day2)


	result1 = Wx_Data((air1_min, air1_max), wind1, (pressure1_min, pressure1_max), precip1, wx1, day1_date)
	result2 = Wx_Data((air2_min, air2_max), wind2, (pressure2_min, pressure2_max), precip2, wx2, day2_date)
	return result1, result2
	
#get_2day_weather_history("nashua nh")


