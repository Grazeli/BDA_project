#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import requests
import pandas as pd
import json
import os

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

    def insert(self, dir_name):
        count_articles = 0
        count_existing = 0

        entries = os.listdir(dir_name+'/')

        count_entries = 0
        for entry in entries:
            count_entries += 1
            print(f'{count_entries} / {len(entries)}')
            #print(entry)
            for file in os.listdir(dir_name+'/'+entry):
                if file.endswith(".txt"):
                    #print(os.path.join(file))
                    #print(os.path.join(entry, file))
                    #f = open('./Data/2021-11-17/2021-11-17_abc-news_abc-news-au_aftenposten.txt')  # open a file
                    f = open('./'+dir_name+'/'+os.path.join(entry, file))  # open a file
                    
                    text = f.read()
                    #print (json.loads(text)['articles'])
                    covid_articles =json.loads(text)['articles']
                    #print(response)

                    count_articles += len(covid_articles)
                    for i in covid_articles:
                        if 'url' in i:
                            del i['url']
                            del i['urlToImage']
                        existing_document =self._collection.find_one(i)
                        if not existing_document:
                             post_id = self._collection.insert_one(i).inserted_id
                        else:
                            count_existing += 1

                        #return post_id
        print('Number of documents: ', count_articles)
        print('Number of duplicates: ', count_existing)
        print("done")


mongo_db = MongoDB(database_name='Covid_db22', collection_name='covid_data22')

mongo_db.insert('Data')

