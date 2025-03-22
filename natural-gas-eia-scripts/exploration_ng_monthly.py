import requests
import json
import csv
import os
import datetime
import pandas as pd

api_key = ""

init_year = 1973

route2 = {"drill": "crude_oil_and_ng_drilling_activity", 
          "wellend": "crude_oil_and_ng_exploratory_and_developement",
          "seis": "max_us_active_seismic_crew_counts"}

for route in route2:
    for year in range(init_year, 2025):
        for month in range(1,13):
            savedir = f"natural_gas/exploration_and_reserves/{route2[route]}/monthly/"
            startyear = str(year)
            endyear = str(year)
            startmonth = str(month)
            endmonth = str(month +1)
            if month < 10:
                startmonth = "0" + startmonth
            if (month+1) < 10:
                endmonth = "0" + endmonth
            if month == 12:
                endmonth = "01"
                endyear = str(year+1)

            # Save file
            directory = savedir
            filename = savedir + startyear + "_" + startmonth + f"_{route}_monthly.csv"

            # Define the API endpoint
            url = ('https://api.eia.gov/v2/natural-gas/enr/'+route+'/data/?'
                    'frequency=monthly'
                    '&data[0]=value'
                    '&start='+startyear+'-'+startmonth+''
                    '&end='+endyear+'-'+endmonth+''
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
            if data['response']['total']:
                with open(filename, 'w', newline='') as csvfile:
                    print(data['response']['total'])
                    # fieldnames = data['response']['data'][0].keys()  # Extract field names from the first dictionary
                    df = pd.DataFrame(data['response']['data'])
                    df.to_csv(filename, index=False)