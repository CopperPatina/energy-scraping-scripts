import requests
import json
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--url')
parser.add_argument('-f', '--filename')
args = parser.parse_args()

url = args.url
dest = args.filename
api_key = "4cD9mA5UNd3SKCxbONA6Cmz48qMIVJ9u9r1vqc78"

geturl = f"{url}&api_key={api_key}"


response = requests.get(geturl)

if response.status_code != 200:
    print("ERROR")
    exit
data = response.json()

with open(f"/Users/kathryn/EIA/{dest}", 'w', newline='') as csvfile:
    json.dump(data, csvfile)
