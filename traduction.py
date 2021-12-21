from pymongo import MongoClient
import pickle
from googletrans import Translator
import googletrans

client = MongoClient(host='localhost', port=27017, maxPoolSize=200)
covidDB = client['Covid_db22'].covid_data22

print(covidDB.count_documents({}))

with open('id_language_dict.pkl', 'rb') as f:
    loaded_dict = pickle.load(f)

need_translation = []

# Changes to make in language: (looked through sources to make sure they matched)
# zh -> zh-cn
# se -> sv
# ud -> ur

for key in loaded_dict:
    if loaded_dict[key] != 'en':
        need_translation.append(key)

    if loaded_dict[key] == 'zh':
        loaded_dict[key] = 'zh-cn'

    if loaded_dict[key] == 'se':
        loaded_dict[key] = 'sv'

    if loaded_dict[key] == 'ud':
        loaded_dict[key] = 'ur'

translator = Translator()

count = 0
len_query = covidDB.count_documents({'source.id': {'$in': need_translation}})

print(need_translation)

# 3 columns need translation: title, description & content
for obj in covidDB.find({'source.id': {'$in': need_translation}}):

    if count % 100 == 0:
        print(f'{count} / {len_query}')
        pass
    count += 1

    if obj['title']:
        covidDB.update_one({'_id': obj['_id']},
                           {'$set':
                                {
                                    'title': translator.translate(obj['title'], dest='en', src=loaded_dict[obj['source']['id']]).text,
                                    'content': translator.translate(obj['content'], dest='en', src=loaded_dict[obj['source']['id']]).text
                                 }
                           })

    if obj['description']:
        covidDB.update_one({'_id': obj['_id']},
                           {'$set':
                                {'description': translator.translate(obj['description'], dest='en', src=loaded_dict[obj['source']['id']]).text,
                                 }})
