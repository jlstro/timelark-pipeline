import requests
import logging
import json

# Set up logging for the module
logger = logging.getLogger(__name__)


def build_aleph_url(host, collection_ids, schema, limit, query):
    base_url = f'{host}/api/2/entities'
    
    # Construct the filter parameters for collection IDs
    collection_filters = "&".join([f"filter%3Acollection_id={collection_id}" for collection_id in collection_ids])
    
    # Construct the full URL with parameters
    url = f"{base_url}?{collection_filters}&filter%3Aschemata={schema}&limit={limit}&q={query}"
    return url

def query_aleph(entity, config):
    """
    Queries the Aleph API to retrieve information based on a an entity type and name.
    
    :param entity: A tuple containing the name and the type of an entity
    :param config: Configuration dictionary containing API key, Aleph host, and collection IDs
    """
    
    host = config['host']
    api_key = config['api_key']
    collections = config['collections']
    schema = entity['schema']
    name = entity['name']

    HEADERS = { "Authorization": api_key, "Content-Type": 'application/json', 'Accept-Encoding': 'gzip, deflate, br' }
    url = build_aleph_url(host, collections, schema, 50, name)
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:  # Check if the response is successful
        logger.info(f'Aleph API call successful: {entity}')
        data = json.loads(response.text)
        return data
    else:
        logger.error(f"API call failed: {url}")
        return None

def parse_schema(schema):
    if schema == 'ORG':
        return 'Company'
    elif schema == 'PERSON':
        return 'Person'
    elif schema == 'EVENT':
        return 'Event'
    else:
        return 'LegalEntity'
    
def enrich_entities(entity, config):
    """
    Enriches entity information using the Aleph API data.

    :param entity: a single spacy extracted entity
    :param config: Configuration dictionary containing API key, Aleph host, and collection IDs
    :return: Enriched entity information
    """
    schema = parse_schema(entity['category'])
    name = entity['text']
    enriched_entity = {'name': name, 'schema': schema}
    
    try:
        data = query_aleph(enriched_entity, config)
        if data:
            for result in data['results']:
                for k, v in result['properties'].items():
                    if k in enriched_entity and enriched_entity[k] != result['properties'][k]:
                        enriched_entity[k] = [enriched_entity[k]] + result['properties'][k]
                    else:
                        enriched_entity[k] = result['properties'][k]
        else:
            logger.warning(f"No data received from Aleph API for entity: {entity['text']}")
    except Exception as e:
        logger.error(f"Error during API query for entity {entity['text']}: {e}")
    
    return enriched_entity