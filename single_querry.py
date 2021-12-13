import requests
import json
import os
import pandas as pd

api_key = '068b9bb6202e4caaa52ad3d2d6dbfd63'
#api_key = 'c831b1bf11824a259d16376dcd86a3da'
#api_key = '50fba327ef774555bb169e07edfa5ec2'

prefix_url = 'https://newsapi.org/v2/everything'
sufix_url =  '&apiKey=' + api_key
sorted_by = '&sortBy=popularity'

# Date format YYYY-MM-DD
dates_range = ['2021-12-09', '2021-12-10']

sources = ['abc-news', 'abc-news-au', 'aftenposten', 'al-jazeera-english', 'google-news-ar', 'argaam', 'ars-technica', 'ary-news', 'associated-press', 'australian-financial-review', 'axios', 'bbc-news', 'bbc-sport', 'bild', 'blasting-news-br', 'bleacher-report', 'bloomberg', 'breitbart-news', 'business-insider', 'business-insider-uk', 'buzzfeed', 'google-news-ca', 'cbs-news', 'cnn', 'cnn-es', 'crypto-coins-news', 'der-tagesspiegel', 'die-zeit', 'el-mundo', 'engadget', 'entertainment-weekly', 'espn', 'espn-cric-info', 'financial-post', 'focus', 'football-italia', 'fortune', 'four-four-two', 'fox-news', 'fox-sports', 'globo', 'google-news', 'ansa', 'google-news-au', 'google-news-br', 'cbc-news', 'google-news-fr', 'google-news-in', 'google-news-is', 'the-times-of-india', 'google-news-ru', 'google-news-sa', 'google-news-uk', 'goteborgs-posten', 'gruenderszene', 'hacker-news', 'handelsblatt', 'ign', 'il-sole-24-ore', 'ynet', 'infobae', 'info-money', 'la-gaceta', 'la-repubblica', 'le-monde', 'lenta', 'lequipe', 'les-echos', 'liberation', 'marca', 'mashable', 'medical-news-today', 'msnbc', 'mtv-news', 'mtv-news-uk', 'national-geographic', 'national-review', 'nbc-news', 'news24', 'new-scientist', 'news-com-au', 'newsweek', 'new-york-magazine', 'next-big-future', 'nfl-news', 'nhl-news', 'nrk', 'politico', 'polygon', 'rbc', 'recode', 'reddit-r-all', 'reuters', 'rt', 'rte', 'rtl-nieuws', 'sabq', 'spiegel-online', 'svenska-dagbladet', 't3n', 'talksport', 'techcrunch', 'techcrunch-cn', 'techradar', 'the-american-conservative', 'the-globe-and-mail', 'the-hill', 'the-hindu', 'the-huffington-post', 'the-irish-times', 'the-jerusalem-post', 'the-lad-bible', 'the-next-web', 'the-sport-bible', 'google-news-it', 'the-verge', 'the-wall-street-journal', 'the-washington-post', 'the-washington-times', 'time', 'usa-today', 'vice-news', 'wired', 'wired-de', 'wirtschafts-woche', 'xinhua-net', 'independent', 'la-nacion']

valid = True

# Create directories for output Data
if not os.path.isdir('Data'):
    os.mkdir('Data')

if not os.path.isdir('summary'):
    os.mkdir('summary')

for date_query in dates_range:
    results = []
    date_name = date_query
    added_date = '&from=' + date_query + 'T00:00:00&to=' + date_query + 'T23:59:59'

    new_data_directory_path = 'Data/' + date_query
    if not os.path.isdir(new_data_directory_path):
        os.mkdir(new_data_directory_path)

    for sources_idx in range(0, 44):
        # la-nacion
        if sources_idx == 42:
            source_name = sources[sources_idx * 3]
            source = '&sources=' + sources[sources_idx * 3]
        # independent
        elif sources_idx == 43:
            source_name = sources[(sources_idx-1) * 3 + 1]
            source = '&sources=' + sources[(sources_idx-1) * 3 + 1]
        else:
            source_name = sources[sources_idx * 3] + '_' + sources[sources_idx * 3 + 1] + '_' + sources[sources_idx * 3 + 2]
            source = '&sources=' + sources[sources_idx * 3] + ',' + sources[sources_idx * 3 + 1] + ',' + sources[sources_idx * 3 + 2]

        url = prefix_url + '?q=Covid&pageSize=100' + added_date + source + sorted_by + sufix_url

        response = requests.get(url)

        if response.status_code != 200:
            valid = False
            print(response)
            break

        summary_query = [date_name, source_name, response.json()['totalResults']]
        print(summary_query)
        results.append(summary_query)

        file_name = date_name + '_' + source_name + '.txt'

        with open(new_data_directory_path + '/' + file_name, 'w') as outfile:
            json.dump(response.json(), outfile)

    if not valid:
        break

    summary_day = pd.DataFrame(results)
    summary_file_path = 'summary/summary_' + date_name + '.csv'
    summary_day.to_csv(summary_file_path, header=False)
    print(results)

print('Ended: ', valid)