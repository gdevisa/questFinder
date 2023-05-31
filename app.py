# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, redirect, url_for, request, render_template, flash
import requests
import json
from datetime import datetime, timedelta
import pytz
import os

# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)



def getFirstAvailable():
    # Define your specific time zone
    timezone = pytz.timezone('America/Los_Angeles')

    # Get the current date and time in your time zone
    now = datetime.now(timezone)
    start_time = now + timedelta(hours=1.5)
    end_time = now + timedelta(hours=12)

    # Format the date and time in RFC 3339 format with the UTC offset
    start_time = start_time.strftime('%Y-%m-%dT%H:%M:%S%z')
    end_time = end_time.strftime('%Y-%m-%dT%H:%M:%S%z')
    # Insert the ":" in the UTC offset
    start_time = start_time[:-2] + ':' + start_time[-2:]
    end_time = end_time[:-2] + ':' + end_time[-2:]
    print(start_time, end_time)

    subKey_conundroom = 'ANEA3MNP3R9HXJ7X636YE41550HRLME314D5E3B0035'
    subKey_conundroomtown = 'A3WLLT7NUR9HXJ7X636YE41550E3FRN9176697930CE'
    subKey_schoolofmagic = 'AWFYARR9KR9HXJ7X636YE41550KHNLUA166980F7E73'
    subKeys = [subKey_conundroomtown, subKey_schoolofmagic]

    apiKey = 'AK4TJAE7TR9HXJ7X636YE41550JNTYFL1668EA661C2'
    secretKey = 'L0XK03xvGRpJvTPWOCaBvtcEj7NA27Tc'
    headers = {'Content-Type': 'application/json'}

    results = []

    for subKey in subKeys:
        ### Get productId and NAMES
        url2 = 'https://api.bookeo.com/v2/settings/products'  # API endpoint for availability

        # Set the required parameters for the request
        parameters = {
            'apiKey': subKey,
            'secretKey': secretKey,
        }

        # Send the request
        response = requests.get(url2, params=parameters, headers=headers)

        # Check the response status code
        if response.status_code == 200:
            # Request successful
            #print('Product list request successful!')
            # print('Response:')
            pretty_json = json.dumps(response.json(), indent=4)
            products = {}
            # print(response.json()['data'][0]['name'])
            for i in response.json()['data']:
                products[i['productId']] = i['name']
        # print(products)

        else:
            # Request failed
            print('Availability request failed.')
            print('Response:', response.text)

        ### Check Availability
        url1 = 'https://api.bookeo.com/v2/availability/slots'  # API endpoint for availability

        # Set the required parameters for the request
        parameters = {
            'apiKey': subKey,
            'secretKey': secretKey,
            'startTime': start_time,
            'endTime': end_time,
            'mode': 'backend'
        }

        # Send the request
        response = requests.get(url1, params=parameters, headers=headers)

        # Check the response status code
        if response.status_code == 200:
            # Request successful
            #print('Availability request successful!')
            # print('Response:')
            avail = response.json()
            pretty_json = json.dumps(response.json(), indent=4)
            # print(pretty_json)
        else:
            # Request failed
            print('Availability request failed.')
            print('Response:', response.text)

        data = avail['data']

        updated_data = [item for item in data if item['numSeatsAvailable'] != 0]

        for i in updated_data:
            i['productName'] = products[i['productId']]
        results.extend(updated_data)
        #print(json.dumps(data[0], indent=4))

    """date1 = datetime.strptime(results[0]['startTime'], '%Y-%m-%dT%H:%M:%S%z')
    date2 = datetime.strptime(results[1]['startTime'], '%Y-%m-%dT%H:%M:%S%z')

    # Compare the dates and get the earlier one
    earlier_date = min(date1, date2)

    final = []

    for i in results:
        if datetime.strptime(i['startTime'], '%Y-%m-%dT%H:%M:%S%z') == earlier_date:
            final.append(i)
    """
    sorted_list = sorted(results, key=lambda x: datetime.strptime(x['startTime'], '%Y-%m-%dT%H:%M:%S%z'))
    response = []

    for i in sorted_list:
        a = 'Name: ' + i['productName'] + ', Start Time: ' + datetime.strptime(i['startTime'], '%Y-%m-%dT%H:%M:%S%z').strftime('%m-%d %H:%M') + ', Num Seats Avail: ' + str(i['numSeatsAvailable']) + '\n'
        response.append(a)

    return response


# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def index(response=None):
    return render_template('index.html', response=response)

@app.route('/', methods=['POST'])
def index_post():
    message = getFirstAvailable()

    if message is None:
        flash('Error')
        return redirect(url_for('app.index'))

    return render_template('index.html', response=message)

# main driver function
"""if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    app.run()"""