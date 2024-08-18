
from typing import Dict, List, Union

import numpy as np
from elasticsearch import Elasticsearch, exceptions


# @data_loader
def search(*args, **kwargs) -> List[Dict]:
    """
    query_embedding: Union[List[int], np.ndarray]
    """
    connection_string = kwargs.get('connection_string', 'http://0.0.0.0:9200')
    # index_name = kwargs.get('index_name', 'documents_20240818_5818')
    index_name = kwargs.get('index_name', 'documents_20240818_0818')
    
    top_k = kwargs.get('top_k', 5)
    chunk_column = kwargs.get('chunk_column', 'document_id')
    query = "When is the next cohort?"
    es_client = Elasticsearch(connection_string)
    es_client.indices.get_alias()
    
    try:
        response = es_client.search(
            index=index_name,
            body={
                "size": top_k,
                "query": {
                    "bool": {
                        "must": {
                            "multi_match": {
                                "query": query,
                                "fields": ["question", "text"],
                                "type": "best_fields"
                            }
                        }
                    }
                }
            }
        )
        

        print(f"Raw response from Elasticsearch: {response}")
        return [hit['_source'][chunk_column] for hit in response['hits']['hits']]
    
    except exceptions.BadRequestError as e:
        print(f"BadRequestError: {e.info}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []

    
if __name__ == "__main__":
    search()