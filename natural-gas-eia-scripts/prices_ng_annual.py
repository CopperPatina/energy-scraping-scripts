import requests
import json
import csv
import os
import datetime
import pandas as pd

api_key = ""
init_year = 1925

# monthly: drill, wellend, seis

route2 = {"sum": "natural_gas_prices",
          "rescom": "avg_price_to_consumers"}

for route in route2:
    for year in range(init_year, 2026):
        savedir = f"natural_gas/prices/{route2[route]}/annual/"
        startyear = str(year)
        endyear = str(year+1)

        # Save file
        directory = savedir
        filename = savedir + str(year)  + f"_{route}_annual.csv"

        # Define the API endpoint
        url = ('https://api.eia.gov/v2/natural-gas/pri/'+route+'/data/?'
                'frequency=annual'
                '&data[0]=value'
                '&start='+startyear+''
                '&end='+endyear+''
                '&sort[0][column]=period'
                '&sort[0][direction]=desc'
                '&offset=0'
                '&length=5000'
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
        print(data['response']['total'])
        if int(data['response']['total']) != 0:
            print("NOT 0, writing")
            with open(filename, 'w', newline='') as csvfile:
                # fieldnames = data['response']['data'][0].keys()  # Extract field names from the first dictionary
                df = pd.DataFrame(data['response']['data'])
                df.to_csv(filename, index=False)