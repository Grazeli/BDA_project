#!/usr/bin/env python
# coding: utf-8

# In[12]:


import requests
import pandas as pd

try:
    from pymongo import MongoClient
except ImportError:
    raise ImportError('PyMongo is not installed')


class MongoDB(object):
    def __init__(self, host='localhost', port=27017, database_name=None, collection_name=None):
        try:
            self._connection = MongoClient(host=host, port=port, maxPoolSize=200)
        except Exception as error:
            raise Exception(error)
        self._database = None
        self._collection = None
        if database_name:
            self._database = self._connection[database_name]
        if collection_name:
            self._collection = self._database[collection_name]

    def insert(self, post):
        # add/append/new single record
        post_id = self._collection.insert_one(post).inserted_id
        return post_id



# In[ ]:


for value in data:
    if 'author,title,publishedAt,content' not in value:
        if value:
            value = value.split(',')
            data_list.append({'author':(value[0]), 'title': (value[1]), 'publishedAt': (value[2]),'content': (value[3])})

print(data_list)

print('[*] Pushing data to MongoDB ')
mongo_db = MongoDB(database_name='CovidNews_DB', collection_name='news_data')

for collection in data_list:
    print('[!] Inserting - ', collection)
    mongo_db.insert(collection)


# In[18]:


api_key='d9428cf2f0ea4deb8ec9348c6a0b9f85'
prefix_url = 'https://newsapi.org/v2/everything'
sufix_url =  '&pageSize=100&apiKey=' + api_key

url = prefix_url + '?q=Covid' + sufix_url
pages = list(range(0, 300677))
pages_list = pages[0:300677:20]

client = MongoClient('127.0.0.1', 27017)
db_name = 'covidAnalytics'

# connect to the database
db = client[db_name]

# open the specific collection
covidData = db.covidData

def get_data(url_base, num_pages,  collection):
    
   
    response = requests.get(url_base).json()

        #print(response)
    covid_articles = response['articles']


    for i in covid_articles:
        if 'url' in i:
            del i['url']
            del i['urlToImage']
        existing_document = collection.find_one(i)
        if not existing_document:
            collection.insert_one(i)
     

                #print("Data Inserted")


# In[20]:


#day one 
get_data(url, pages_list,  covidData)
db.covidData.count()


# In[22]:


#day one
#no restriction for date
url2 = prefix_url + '?q=vaccin' + sufix_url
get_data(url2, pages_list,  covidData)


# In[26]:


#day two
#add news from today: 09/12/2021  for covid
date_today='2021-12-09'
url3=prefix_url + '?q=covid' + sufix_url+'&from='+date_today
get_data(url3, pages_list,  covidData)


# In[27]:


#add news from today: 09/12/2021  for vaccin
url4=prefix_url + '?q=vaccin' + sufix_url+'&from='+date_today
get_data(url4, pages_list,  covidData)


# In[28]:


date_yesterday='2021-12-08'
url5=prefix_url + '?q=covid' + sufix_url+'&from='+date_yesterday
url6=prefix_url + '?q=vaccin' + sufix_url+'&from='+date_yesterday
get_data(url5, pages_list,  covidData)
get_data(url6, pages_list,  covidData)


# In[31]:


other_date='2021-12-07'
url7=prefix_url + '?q=covid' + sufix_url+'&from='+other_date
url8=prefix_url + '?q=vaccin' + sufix_url+'&from='+other_date
get_data(url7, pages_list,  covidData)
get_data(url8, pages_list,  covidData)


# now we have collected enough data :  575 documents of news from one month ago (fresh news) that are related to covid19 and vaccine

# In[ ]:




