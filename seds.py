import requests
import json
import csv
import os
import datetime
import pandas as pd

api_key = "4cD9mA5UNd3SKCxbONA6Cmz48qMIVJ9u9r1vqc78"

init_year = 1960

states = [
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA',
    'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA',
    'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY',
    'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
    'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY', 'DC', 'X3', 'X5'
]

# X3 is Gulf of Mexico
# X5 is Pacific

for year in range(init_year, 2025):
    for statename in states:
        savedir = f"seds/{statename}/"
        startyear = str(year)
        endyear = str(year+1)

        # Save file
        directory = savedir
        filename = savedir + startyear + '_' + statename + 'seds_annual.csv'

        # Define the API endpoint
        url = ('https://api.eia.gov/v2/seds/data/?'
                'frequency=annual'
                '&data[0]=value'
                '&facets[stateId][]='+statename+''
                '&start='+startyear+''
                '&end='+endyear+''
                '&sort[0][column]=period'
                '&sort[0][direction]=desc'
                '&offset=0'
                '&length=41000'
                '&api_key='+api_key+'')


        # Make the GET request
        response = requests.get(url)
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
        else:
            print(f"Failed to retrieve data: {response.status_code}")
            print(year)

        if not os.path.exists(directory):
            os.makedirs(directory)

        print(filename)
        with open(filename, 'w', newline='') as csvfile:
            print(data['response']['total'])
            # fieldnames = data['response']['data'][0].keys()  # Extract field names from the first dictionary
            df = pd.DataFrame(data['response']['data'])
            df.to_csv(filename, index=False)