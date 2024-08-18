import requests
import json
from typing import List, Dict

from mage_ai.shared.hash import dig
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def ingest_api_data(*args, **kwargs) -> List[Dict]:
    """
    Template for loading data from an API.
    Fetch data from external API using the provided configurations.

    Args:
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.

    Keyword Args:
        endpoint (str): API endpoint URL.
        auth_token (str): Authentication token for the API.
        method (str): HTTP method to use (GET, POST, etc.).
        timeout (int): Request timeout in seconds.
    """
    endpoint = kwargs.get('endpoint')
    auth_token = kwargs.get('auth_token')
    method = kwargs.get('method', 'GET')
    timeout = kwargs.get('timeout', 30)
    parser = kwargs.get('parser')

    headers = {}
    if auth_token:
        headers['Authorization'] = f"Bearer {auth_token}"

    response = requests.request(
        method=method,
        url=endpoint or  '',
        headers=headers,
        timeout=timeout
    )
    response.raise_for_status()
    result = response.json()

    if parser:
        result = dig(result, parser)

    return [result]


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'