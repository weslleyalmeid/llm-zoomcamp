if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

from typing import Dict, List, Union

import numpy as np
from elasticsearch import Elasticsearch, exceptions


@data_loader
def search(*args, **kwargs) -> List[Dict]:
    """
    query_embedding: Union[List[int], np.ndarray]
    """
    connection_string = kwargs.get('connection_string', 'http://elasticsearch:9200')
    index_name = kwargs.get('index_name', 'documents_20240818_0818')
    top_k = kwargs.get('top_k', 5)
    chunk_column = kwargs.get('chunk_column', 'document_id')
    query = "When is the next cohort?"
    es_client = Elasticsearch(connection_string)
    
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


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'