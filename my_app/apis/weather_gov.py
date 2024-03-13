import requests
import json
from my_app.misc.search_algos import *
import os
import matplotlib.pyplot as plt
from my_app.error_logging import logger



class Wx_Forecast:
    def __init__(self):
        self.wx_data = {"grid_id": None,
                        "grid_x": None,
                        "grid_y": None,
                        "Location_Station": None,
                        "City": None,
                        "State": None,
                        "Lat_N": None,
                        "Lat_S": None,
                        "Lon_E": None,
                        "Lon_W": None,
                        "Elev": None,
                        "Conditions": None,
                        "Temperature_F": None,
                        "Temperature_C": None,
                        "Humidity": None,
                        "Wind_Speed": None,
                        "Wind_Direction": None,
                        "Wind_Gust": None,
                        "Barometer_in": None,
                        "Barometer_mb": None,
                        "Dewpoint_F": None,
                        "Dewpoint_C": None,
                        "Visibility": None,
                        "Heat_Index_F": None,
                        "Heat_Index_C": None,
                        "Wind_Chill_F": None,
                        "Wind_Chill_C": None,
                        "Last_Update": None}


def fahrenheit_to_celsius(fahrenheit):
    celsius = (fahrenheit - 32) * 5/9
    return int(celsius)


def celsius_to_fahrenheit(celsius):
    fahrenheit = (celsius * 9/5) + 32
    return int(fahrenheit)


def parse_time_stamp(data):
    result = data.replace("T", " ")
    return result[:-6]


# get grid id, x, y
def get_grid_info(lat, lon):
    grid_points_url = f"https://api.weather.gov/points/{lat},{lon}"
    try:
        gridId = json.loads(requests.get(grid_points_url).content.decode(
            "UTF-8"))["properties"]["gridId"]
        gridX = json.loads(requests.get(grid_points_url).content.decode(
            "UTF-8"))["properties"]["gridX"]
        gridY = json.loads(requests.get(grid_points_url).content.decode(
            "UTF-8"))["properties"]["gridY"]
    except Exception as e:
        logger.logger.error(f"Check internet connection! get_grid_info()\n\t{e}")
        return None
    print(gridId, gridX, gridY)
    return gridId, int(gridX), int(gridY)

# def get_stations():
#     url = f"https://api.weather.gov/gridpoints/{office}/{gridX},{gridY}/stations"
#     res = requests.get(url).content.decode("UTF-8")

# def get_forecast_daily(office, gridX, gridY):
#     url = f"https://api.weather.gov/gridpoints/{office}/{gridX},{gridY}/forecast"
#     res = requests.get(url).content.decode("UTF-8")
#     #print(res)


def get_forecast_hourly(office, gridX, gridY):
    url = f"https://api.weather.gov/gridpoints/{office}/{gridX},{gridY}/forecast/hourly"
    try:
        res = requests.get(url)
        page = json.loads(res.content)
    except Exception as e:
        logger.logger.error(f"Check internet connection! get_forecast_hourly\n\t{e}")
        return None
    if res.status_code == 200:
        return page
    return None


def parse_hourly(data):
    if not data:
        return
    hourly_data = {}
    hourly_data["Start_Time"] = []
    hourly_data["End_Time"] = []
    hourly_data["Temperature_F"] = []
    hourly_data["Temperature_C"] = []
    hourly_data["Percent_Precipitation"] = []
    hourly_data["Dewpoint_F"] = []
    hourly_data["Dewpoint_C"] = []
    hourly_data["Wind_Speed"] = []
    hourly_data["Wind_Direction"] = []
    hourly_data["Humidity"] = []
    hourly_data["Short_Forecast"] = []

    data_list = data["properties"]["periods"]

    for i, entry in enumerate(data_list):

        hourly_data["Start_Time"].append(parse_time_stamp(entry["startTime"]))

        hourly_data["End_Time"].append(parse_time_stamp(entry["endTime"]))

        hourly_data["Temperature_F"].append(entry["temperature"])

        hourly_data["Temperature_C"].append(
            fahrenheit_to_celsius(entry["temperature"]))

        hourly_data["Percent_Precipitation"].append(
            entry["probabilityOfPrecipitation"]["value"])

        hourly_data["Dewpoint_F"].append(
            round(celsius_to_fahrenheit(entry["dewpoint"]["value"])))

        hourly_data["Dewpoint_C"].append(round(entry["dewpoint"]["value"]))

        hourly_data["Humidity"] .append(entry["relativeHumidity"]["value"])

        hourly_data["Wind_Speed"].append(
            extract_nums_from_str(entry["windSpeed"])[0])
        hourly_data["Wind_Direction"].append(entry["windDirection"].lower())

        hourly_data["Short_Forecast"].append(entry["shortForecast"])

    return hourly_data


def plot_1_line(data, hi_lo=None, title="Title", x_label="X Label", y_label="Y Label", line_label="Line", x_increment=12, y_increment=4, value_fnt_size=14,
                 tick_fnt_size=16, legend_fnt_size=16, label_fnt_size=16, title_fnt_size=24, y_min=None, y_max=None, value_color="red", x_tick_values=None, title_color="red"):
    if not x_tick_values:
        x_tick_values = range(len(data))
    y = data

    # Create a figure and axis
    fig, ax = plt.subplots()

    # Set axis labels and title
    plt.title(title, fontsize=title_fnt_size, fontweight="bold", color=title_color)
    plt.xlabel(x_label, fontsize=label_fnt_size, color="blue")
    plt.ylabel(y_label, fontsize=label_fnt_size, color="blue")

    # Plot the line
    plt.plot(x_tick_values, y, label=line_label, color="orange")

    # Add a legend
    # ax.legend([title], fontsize=legend_fnt_size)

    # Set x-axis limit to start at 0
    plt.xlim(left=0, right=x_tick_values[-1])

    # get mins and max of data
    if not y_min and not y_max:
        y_min = min(y)
        y_max = max(y)

    # set y-tick values and add horizontal grid lines
    plt.yticks(range(y_min, y_max + 1, y_increment), fontsize=tick_fnt_size)
    plt.grid(axis='y', linestyle='--', color='lightgray')

    # Set x-tick values and add vertical grid lines
    x_tick_locations = list(x_tick_values[::x_increment]) + [x_tick_values[-1]]
    plt.xticks(x_tick_locations, fontsize=tick_fnt_size)
    plt.grid(axis='x', linestyle='--', color='lightgray')

    # Line values for last x_tick
    last_x_tick = x_tick_values[-1]
    last_y_value = y[-1]

    # Add text annotations at each x-tick value
    ha = "left"
    va = "top"
    x_tickval_increment_length = len(x_tick_values[::x_increment])
    if hi_lo:
        for x, y in hi_lo:
            if x == 0:
                ha = "left"
                plt.text(x, y, str(y), ha=ha, va=va,
                         fontsize=value_fnt_size, color=value_color)
            elif x == len(data) - 1:
                ha = "right"
                plt.text(x, y, str(y), ha=ha, va=va,
                         fontsize=value_fnt_size, color=value_color)
            else:
                ha = "left"
                plt.text(x, y, str(y), ha=ha, va=va,
                         fontsize=value_fnt_size, color=value_color)
    if hi_lo is None:
        ha = "left"
        for cnt, val in enumerate(zip(x_tick_values[::x_increment], data[::x_increment])):
            x, y = val
            if cnt == x_tickval_increment_length-1 and data[x] == data[-1]:
                ha = "right"
                plt.text(x, y, str(y), ha=ha, va=va,
                         fontsize=value_fnt_size, color=value_color)
            elif cnt == x_tickval_increment_length-1 and data[x] != data[-1]:
                ha = "left"
                plt.text(x, y, str(y), ha=ha, va=va,
                         fontsize=value_fnt_size, color=value_color)
                ha = "right"
                plt.text(last_x_tick, last_y_value, str(
                    last_y_value), ha=ha, va=va, fontsize=value_fnt_size, color=value_color)
            else:
                plt.text(x, y, str(y), ha=ha, va=va,
                         fontsize=value_fnt_size, color=value_color)

    temp_title = title.lower().replace(" ", "_")
    out_file = f'my_app/static/pics/{temp_title}_graph.png'
    plt.savefig(out_file)



def plot_2_lines(data, hi_lo=None, title="Title", x_label="X Label", y_label="Y Label", line1_label="Line 1", line2_label="Line 2",  x_increment=12, y_increment=4, value_fnt_size=14,
                 tick_fnt_size=16, legend_fnt_size=16, label_fnt_size=16, title_fnt_size=24):
    x_tick_values = range(len(data[0]))
    temp_y = data[0]
    dew_y = data[1]
    # Create a figure and axis
    fig, ax = plt.subplots()

    # Set axis labels and title
    plt.title(title, fontsize=title_fnt_size, fontweight="bold", color="red")
    plt.xlabel(x_label, fontsize=label_fnt_size, color="blue")
    plt.ylabel(y_label, fontsize=label_fnt_size, color="blue")

    # Plot the first line
    ax.plot(x_tick_values, temp_y, label=line1_label, color="orange")
    # Plot the second line
    ax.plot(x_tick_values, dew_y, label=line2_label, color="lightblue")
    # Add a legend
    ax.legend(fontsize=legend_fnt_size)

    # Set x-axis limit to start at 0
    plt.xlim(left=0, right=x_tick_values[-1])

    # get mins and max of data
    temp_min = min(temp_y)-3
    dew_min = min(dew_y)-3
    temp_max = max(temp_y) + 10
    dew_max = max(dew_y) + 10
    y_max = max(temp_max, dew_max)
    y_min = min(temp_min, dew_min)

    # set y-tick values and add horizontal grid lines
    plt.yticks(range(y_min, y_max + 1, y_increment), fontsize=tick_fnt_size)
    plt.grid(axis='y', linestyle='--', color='lightgray')

    # Set x-tick values and add vertical grid lines
    x_tick_locations = list(x_tick_values[::x_increment]) + [x_tick_values[-1]]
    plt.xticks(x_tick_locations, fontsize=tick_fnt_size)
    plt.grid(axis='x', linestyle='--', color='lightgray')

    # Line values for last x_tick
    last_x_tick = x_tick_values[-1]
    last_line1_value = temp_y[-1]
    last_line2_value = dew_y[-1]

    # Add text annotations at each x-tick value for Temp(red) and Dew(brown)
    cnt = 0
    ha = "left"
#    va = "center"
    va = "top"
#    va = "bottom"
#    va = "baseline"
    x_tickval_increment_length = len(x_tick_values[::x_increment])
    if hi_lo:
        for x, y in hi_lo:
            # plt.title(f"VA: {va}", fontsize=40, fontweight="bold", color="red")
            # if x % 2 == 1:
            # va = "top"
            # else:
            # va = "bottom"
            if x == 0:
                ha = "left"
                plt.text(x, dew_y[x], str(dew_y[x]), ha=ha,
                         va=va, fontsize=value_fnt_size, color="brown")
                plt.text(x, y, str(y), ha=ha, va=va,
                         fontsize=value_fnt_size, color="red")
            elif x == len(temp_y)-1:
                ha = "right"
                plt.text(x, dew_y[x], str(dew_y[x]), ha=ha,
                         va=va, fontsize=value_fnt_size, color="brown")
                plt.text(x, y, str(y), ha=ha, va=va,
                         fontsize=value_fnt_size, color="red")
            else:
                ha = "left"
                plt.text(x, dew_y[x], str(dew_y[x]), ha=ha,
                         va=va, fontsize=value_fnt_size, color="brown")
                plt.text(x, y, str(y), ha=ha, va=va,
                         fontsize=value_fnt_size, color="red")
    else:
        # Add text annotations at each x-tick value for Temp
        x_tickval_increment_length = len(x_tick_values[::x_increment])
        cnt = 0
        ha = "left"
        for cnt, val in enumerate(zip(x_tick_values[::x_increment], temp_y[::x_increment])):
            x, y = val
            if cnt == x_tickval_increment_length-1 and temp_y[x] == temp_y[-1]:
                ha = "right"
                plt.text(x, y, str(y), ha=ha, va=va,
                         fontsize=value_fnt_size, color="red")
            elif cnt == x_tickval_increment_length-1 and temp_y[x] != temp_y[-1]:
                ha = "left"
                plt.text(x, y, str(y), ha=ha, va=va,
                         fontsize=value_fnt_size, color="red")
                ha = "right"
                plt.text(last_x_tick, last_line1_value, str(
                    last_line1_value), ha=ha, va=va, fontsize=value_fnt_size, color="red")
            else:
                plt.text(x, y, str(y), ha=ha, va=va,
                         fontsize=value_fnt_size, color="red")
            cnt += 1

#     Add text annotations at each x-tick value for Dew
        cnt = 0
        ha = "left"
        for cnt, val in enumerate(zip(x_tick_values[::x_increment], dew_y[::x_increment])):
            # plt.title(f"{x} {y} Last2: {last_line2_value} Last1: {last_line1_value}", fontsize=40, fontweight="bold", color="red")
            x, y = val
            if cnt == x_tickval_increment_length-1 and dew_y[x] == dew_y[-1]:
                ha = "right"
                plt.text(x, y, str(y), ha=ha, va=va,
                         fontsize=value_fnt_size, color="brown")
            elif cnt == x_tickval_increment_length-1 and dew_y[x] != dew_y[-1]:
                plt.text(x, y, str(y), ha=ha, va=va,
                         fontsize=value_fnt_size, color="brown")
                ha = "right"
                plt.text(last_x_tick, last_line2_value, str(
                    last_line2_value), ha=ha, va=va, fontsize=value_fnt_size, color="brown")
            else:
                plt.text(x, y, str(y), ha=ha, va=va,
                         fontsize=value_fnt_size, color="brown")
            cnt += 1
    plt.savefig('my_app/static/pics/temp_dew_3day_graph.png')
#    plt.show()


def find_peaks_valleys(data):
    peaks_valleys = []
    peaks_valleys.append((0, (data[0])))
    direction = None

    for i in range(1, len(data)):
        if i == len(data)-1:
            peaks_valleys.append((i, (data[i])))

        if data[i-1] > data[i] and direction is None:
            if direction is None:
                direction = "down"
        if data[i-1] < data[i] and direction is None:
            if direction is None:
                direction = "up"
        # down -> up
        if data[i-1] < data[i] and direction == "down":
            direction = "up"
            peaks_valleys.append((i-1, data[i-1]))

        # up -> down
        if data[i-1] > data[i] and direction == "up":
            direction = "down"
            peaks_valleys.append((i-1, data[i-1]))

    return peaks_valleys


def peaks_valleys_24hr(data):
    peaks_valleys = []
    peaks_valleys.append((0, (data[0])))
    max_val = -999999
    min_val = 999999
    for i, val in enumerate(data):
        if i % 24 == 0:
            max_val = -999999
            min_val = 999999
        if val > max_val:
            max_val = val
        if val < min_val:
            min_val = val
        if i == len(data)-1:
            peaks_valleys.append((i, data[i]))



def get_forecast_graph(lat, lon):
    # Nashua NH coord for testing
#     lat = 42.8356421
#     lon = -71.6473598
    #print(f"Lat: {lat}, Lon: {lon}")

    files_to_delete = ["/home/bfair/Desktop/working_desktop/myDesktop/Coding Dojo/Python Stack/PyMySQLProjects/python_app_projects/my_app/static/pics/3_day_temperature_graph.png",
                        "/home/bfair/Desktop/working_desktop/myDesktop/Coding Dojo/Python Stack/PyMySQLProjects/python_app_projects/my_app/static/pics/3_day_humidity_graph.png", 
                        "/home/bfair/Desktop/working_desktop/myDesktop/Coding Dojo/Python Stack/PyMySQLProjects/python_app_projects/my_app/static/pics/3_day_precipitation_graph.png"]
    for file_path in files_to_delete:
        try:
            os.remove(file_path)
            print(f'The file {file_path} has been deleted successfully.')
        except OSError as e:
            logger.logger.error(f"File Deletion Error: {e.filename} - {e.strerror}")

    grid_data = get_grid_info(lat, lon)
    if not grid_data:
        return False
    gridId, gridX, gridY = grid_data
    raw_data = get_forecast_hourly(gridId, gridX, gridY)
    if not raw_data:
        return False
    hourly_data = parse_hourly(raw_data)
    graphing_data = [hourly_data["Temperature_F"][:73],  hourly_data["Humidity"][:73], hourly_data["Percent_Precipitation"][:73]]
    temp_peaks_valleys = find_peaks_valleys(graphing_data[0])
    humidity_peaks_valleys = find_peaks_valleys(graphing_data[1])
    pop_peaks_valleys = find_peaks_valleys(graphing_data[2])
    x_label = "Time From Last Refresh (hrs)"

    plot_1_line(graphing_data[0], hi_lo=0, title="3 Day Temperature", x_label=x_label, y_label="Temperature (F)", x_increment=12, y_increment=3, value_fnt_size=14,
                 tick_fnt_size=16, legend_fnt_size=16, label_fnt_size=16, title_fnt_size=24)
    
    plot_1_line(graphing_data[1], hi_lo=0, title="3 Day Humidity", x_label=x_label, y_label="Humidity (%)", x_increment=12, y_increment=10, value_fnt_size=14,
                 tick_fnt_size=16, legend_fnt_size=16, label_fnt_size=16, title_fnt_size=24, y_min=0, y_max=100)
    
    plot_1_line(graphing_data[2], hi_lo=0, title="3 Day Precipitation", x_label=x_label, y_label="Precipitation (%)", x_increment=12, y_increment=10, value_fnt_size=14,
               tick_fnt_size=16, legend_fnt_size=16, label_fnt_size=16, title_fnt_size=24, y_min=0, y_max=100)
    return True
    
