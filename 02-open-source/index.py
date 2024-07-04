from elasticsearch import Elasticsearch
import os
import json
from tqdm.auto import tqdm

with open('documents.json', 'rt') as f_in:
    docs_raw = json.load(f_in)
    

documents = []

for course_dict in docs_raw:
    for doc in course_dict['documents']:
        doc['course'] = course_dict['course']
        documents.append(doc)

es_client = Elasticsearch('http://localhost:9200')



index_settings = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0
    },
    "mappings": {
        "properties": {
            "text": {"type": "text"},
            "section": {"type": "text"},
            "question": {"type": "text"},
            "course": {"type": "keyword"} 
        }
    }
}

index_name = "course-questions"

try:
    es_client.indices.create(index=index_name, body=index_settings)
    print("Index created successfully!")
except Exception as e:
    print("Error creating index:", e)
    
for doc in tqdm(documents):
    es_client.index(index=index_name, document=doc)