import requests
from bs4 import BeautifulSoup as BS
from googlesearch import search
from my_app.error_logging import logger


def get_soup(url):
	soup = None
	try:
		res = requests.get(url)
		soup = BS(res.content, "html.parser")
	except Exception as e:
		logger.logger.error(f"Check internet connection! get_soup()\n\t{e}")
	return soup
	
def get_url(city_state):
	query = f"{city_state} forecast.weather.gov"
	try:
		search_results = search(query, num_results=10, sleep_interval=.3)
	except Exception as e:
		logger.logger.error(f"Google Search error! get_url()\n\t{e}")

	result = ""
	for i, url in enumerate(search_results):
		if "https://forecast.weather.gov/MapClick.php?lat" in url:
			city, state = city_state.split(" ")
			cap_city = capitalize_city(city)
			res = find_substring(cap_city, url)
			if res:
				result = url
				break
			else:
				result = url
				break
	return result


def parse_station_code(data):
	station = ""
	for i, char in enumerate(data):
		if char == "(":
			station = data[i+1]+data[i+2]+data[i+3]+data[i+4]
			break
	return station

	
def get_station_code(soup):
	current_conditions = soup.find(id="current-conditions")
	panel_headings = current_conditions.find_all(class_="panel-heading")
	station_str = panel_headings[0].find("h2")
	station = parse_station_code(station_str.text)
	return station
	

def find_substring(substring, the_string):
	if not substring or not the_string:
		return
	substring = substring.lower()
	the_string = the_string.lower()
	temp_substring = ""
	index = 0
	current_char = substring[index]

	for i in range(len(the_string)):
		if the_string[i] != current_char:
			temp_substring = ""
			current_char = substring[0]
			index = 0
		if the_string[i] == current_char:
#			print(f"current_char: {current_char}\nthe_string[i]: {the_string[i]}")
			temp_substring += the_string[i]
			if index < len(substring)-1:
				index += 1
				current_char = substring[index]
		if temp_substring == substring:
#			print(f"Found substring '{substring}'")
			return i-len(temp_substring)
#	print(f"Substring '{substring}' not found...")
	return False


def capitalize_city(city):
	char = city[0].upper()
	result = char + city[1:]
	return result


def get_station_code_from_city_state(city_state):
	url = get_url(city_state)
	soup = get_soup(url)
	station = get_station_code(soup)
	print(station)
	return station


# def main():
# 	get_station_code_from_city_state("Rochester nh")

# if __name__ == "__main__":
# 	main()