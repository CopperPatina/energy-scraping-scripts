import requests
import json
import csv
import os
import datetime
import pandas as pd

api_key = ""
init_year = 1925

route2 = {"impc": "us_ng_imports_by_country",
          "expc": "us_ng_exports_reexports_by_country",
          "state": "us_ng_imports_exports_by_state",
          "poe1": "us_ng_imports_point_of_entry",
          "poe2": "us_ng_exports_reexports_point_of_exit",
          "ist": "intl_interstate_movement_ng_by_state"
          }

for route in route2:
    for year in range(init_year, 2026):
        savedir = f"natural_gas/imports_exports_pipelines/{route2[route]}/annual/"
        startyear = str(year)
        endyear = str(year+1)

        # Save file
        directory = savedir
        filename = savedir + str(year)  + f"_{route}_annual.csv"

        # Define the API endpoint
        url = ('https://api.eia.gov/v2/natural-gas/move/'+route+'/data/?'
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