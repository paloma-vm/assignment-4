import os
import requests

from pprint import PrettyPrinter
from datetime import datetime, timedelta
from dotenv import load_dotenv
from flask import Flask, render_template, request, send_file
# from geopy.geocoders import Nominatim
# it wouldn't load or download


################################################################################
## SETUP
################################################################################

app = Flask(__name__)

# Get the API key from the '.env' file
load_dotenv()

pp = PrettyPrinter(indent=4)

API_KEY = os.getenv('API_KEY')
API_URL = 'http://api.openweathermap.org/data/2.5/weather'




################################################################################
## ROUTES
################################################################################

@app.route('/')
def home():
    """Displays the homepage with forms for current or historical data."""
    context = {
        'min_date': (datetime.now() - timedelta(days=5)),
        'max_date': datetime.now()
    }
    return render_template('home.html', **context)

def get_letter_for_units(units):
    """Returns a shorthand letter for the given units."""
    return 'F' if units == 'imperial' else 'C' if units == 'metric' else 'K'

def get_rate_letter(units):
    """Returns a shorthand rate for the given units."""
    return 'mph' if units == 'imperial' else 'm/s' if units == 'metric' else 'm/s'

@app.route('/results')
def results():
    """Displays results for current weather conditions."""
    # TODO: Use 'request.args' to retrieve the city & units from the query
    # parameters.
    city = request.args.get('city')
    units = request.args.get('units')#why the red line?
    

    params = {
        # TODO: Enter query parameters here for the 'appid' (your api key),
        # the city, and the units (metric or imperial).
        # See the documentation here: https://openweathermap.org/current
        'appid': API_KEY,
        'q': city,
        'units': units

    }

    result_json = requests.get(API_URL, params=params).json()

    # current_time = datetime.now()
    # date = current_time.strftime('%A, %B %d, %Y')
    # this did not work, I'm not sure why

    # Uncomment the line below to see the results of the API call!
    pp.pprint(result_json)

    # TODO: Replace the empty variables below with their appropriate values.
    # You'll need to retrieve these from the result_json object above.

    # For the sunrise & sunset variables, I would recommend to turn them into
    # datetime objects. You can do so using the `datetime.fromtimestamp()` 
    # function.
    context = {
        # 'date_form': datetime.fromtimestamp(result_json['dt']),
        'date': datetime.now().strftime('%A, %B %d, %Y'),#got help from Jane
        'city': result_json['name'],
        'description': result_json['weather'][0]['description'],
        'temp': result_json['main']['temp'],
        'humidity': result_json['main']['humidity'],
        'wind_speed': result_json['wind']['speed'],
        'sunrise': datetime.fromtimestamp(result_json['sys']['sunrise']),
        'sunset': datetime.fromtimestamp(result_json['sys']['sunset']),
        'units_letter': get_letter_for_units(units),
        'rate_letter': get_rate_letter(units)    

    }

    return render_template('results.html', **context)


def make_api_call(city, units):
    """makes api call for a city and stores info in a dict"""
    params = {
        'appid': API_KEY,
        'q': city,
        'units': units
    }
    result_json = requests.get(API_URL, params=params).json()

    return result_json



@app.route('/comparison_results')
def comparison_results():
    """Displays the relative weather for 2 different cities."""
    # TODO: Use 'request.args' to retrieve the cities & units from the query
    # parameters.
    city1 = request.args.get('city1')
    city2 = request.args.get('city2')
    units = request.args.get('units')

    # TODO: Make 2 API calls, one for each city. HINT: You may want to write a 
    # helper function for this!
    
    # TODO: Pass the information for both cities in the context. Make sure to
    # pass info for the temperature, humidity, wind speed, and sunset time!
    # HINT: It may be useful to create 2 new dictionaries, `city1_info` and 
    # `city2_info`, to organize the data.
    city1_info = make_api_call(city1, units)
    city2_info = make_api_call(city2, units)

    temp_1 = city1_info['main']['temp']
    temp_2 = city2_info['main']['temp']

    humidity_1 = city1_info['main']['humidity']
    humidity_2 = city2_info['main']['humidity']

   
    num_degrees = "{:.2f}".format(float(temp_1 - temp_2))
    abs_num_degrees = abs(float(num_degrees))

    warmer_or_colder = ''
    if temp_1 > temp_2:
        warmer_or_colder = "warmer"
    if temp_1 < temp_2:
        warmer_or_colder = "colder"
    if temp_1 == temp_2:
        warmer_or_colder = "the same temperature as"


    humidity_diff = float(humidity_1 - humidity_2)
    abs_humidity_diff = abs(humidity_diff)

    humidity_greater_or_less = ''
    if humidity_1 > humidity_2:
        humidity_greater_or_less = "greater"
    if humidity_1 < humidity_2:
        humidity_greater_or_less = "less"
    if humidity_1 ==humidity_2:
        humidity_greater_or_less = "the same humidity as"

    # the difference between their percentages is

    wind_speed_1 = city1_info['wind']['speed']
    wind_speed_2 = city2_info['wind']['speed']

    wind_diff = city1_info['wind']['speed'] - city2_info['wind']['speed']
    wind_greater_or_less = ''
    if wind_speed_1 > wind_speed_2:
        wind_greater_or_less = "greater"
    if wind_speed_1 < wind_speed_2:
        wind_greater_or_less = "less"
    if wind_speed_1 == wind_speed_2:
        wind_greater_or_less = "the same speed as"

    sunset_1 = datetime.fromtimestamp(city1_info['sys']['sunset'])
    sunset_2 = datetime.fromtimestamp(city2_info['sys']['sunset'])

    print(sunset_1)
    print(sunset_2)


    sunset_time_diff = sunset_1 - sunset_2
    # ^ timedelta object
    print(sunset_time_diff)
    print(type(sunset_time_diff))
    # sunset_time_diff_hours = sunset_time_diff / timedelta(hours=1)
    seconds = sunset_time_diff.seconds
    # converts time diff to seconds, help from folkstalk.com
    hours = seconds//3600
    # gets the  amount of whole hours
    minutes = (seconds//60)%60
    # gets the minutes left over
    

    #  num_degrees = "{:.2f}".format(float(temp_1 - temp_2))
    # abs_num_degrees = abs(float(num_degrees))

    
    sunset_time_earlier_or_later = ''
    if sunset_1 > sunset_2:
        sunset_time_earlier_or_later = "later"
    if sunset_1 < sunset_2:
        sunset_time_earlier_or_later = "earlier"
    if sunset_1 == sunset_2:
        sunset_time_earlier_or_later = "the same time as"


    
    context = {
        'city1_info': city1_info,
        'city2_info': city2_info,
        'date': datetime.now().strftime('%A, %B %d, %Y'),#got help from Jane
        'name_1': city1_info['name'],
        'name_2': city2_info['name'],
        'description_1': city1_info['weather'][0]['description'],
        'description_2': city2_info['weather'][0]['description'],
        'temp_1': temp_1,
        'temp_2': temp_2,
        'humidity_1': humidity_1,
        'humidity_2': humidity_2,
        'wind_speed_1': wind_speed_1,
        'wind_speed_2': wind_speed_2,
        # 'sunrise': datetime.fromtimestamp(result_json['sys']['sunrise']),
        # 'sunset_1': datetime.fromtimestamp(city1_info['sys']['sunset']),
        # 'sunset_2': datetime.fromtimestamp(city2_info['sys']['sunset']),
        'sunset_1': sunset_1,
        'sunset_2': sunset_2,
        'units_letter': get_letter_for_units(units),
        'rate_letter': get_rate_letter(units),
        'num_degrees': num_degrees,
        'warmer_or_colder': warmer_or_colder,
        'humidity_diff': humidity_diff,
        'humidity_greater_or_less': humidity_greater_or_less,
        'wind_diff': wind_diff,
        'wind_greater_or_less': wind_greater_or_less,
        'sunset_time_diff': sunset_time_diff,
        'sunset_time_earlier_or_later': sunset_time_earlier_or_later,
        'abs_humidity_diff': abs_humidity_diff,
        'abs_num_degrees': abs_num_degrees,
        'hours': hours,
        'minutes': minutes

    }

    return render_template('comparison_results.html', **context)


if __name__ == '__main__':
    app.config['ENV'] = 'development'
    app.run(debug=True)
