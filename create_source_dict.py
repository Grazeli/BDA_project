import json
import pandas as pd
import pickle

with open ('sources.txt') as f:
    json_sources = json.load(f)

df = pd.DataFrame(json_sources['sources'])

# Create dictionary newspapers ID -> language
df_clean = df[['id', 'language']]

d = {}

for row in df_clean.iterrows():
    d[row[1]['id']] = row[1]['language']

print(d)
with open('id_language_dict.pkl', 'wb') as f:
    pickle.dump(d, f)