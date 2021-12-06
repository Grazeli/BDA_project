import requests
import json

api_key = '068b9bb6202e4caaa52ad3d2d6dbfd63'

prefix_url = 'https://newsapi.org/v2/everything'
sufix_url =  '&apiKey=' + api_key

url = prefix_url + '?q=Covid' + sufix_url

response = requests.get(url)

print(response.json())

with open('data_test.txt', 'w') as outfile:
    json.dump(response.json(), outfile)