import re
import logging
from arango import ArangoClient
from app.config import Config

# List of AQL keywords to avoid
AQL_KEYWORDS = {"FOR", "FILTER", "RETURN", "LET", "SORT", "LIMIT", "COLLECT", "INSERT", "UPDATE", "REPLACE", "REMOVE", "UPSERT"}

# Initialize ArangoDB client
client = ArangoClient(hosts=Config.ARANGO_HOSTS)
db = client.db(Config.ARANGO_DB_NAME, username=Config.ARANGO_USERNAME, password=Config.ARANGO_PASSWORD)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

def clean_key(key: str) -> str:
    key = key.replace(' ', '_')
    key = re.sub(r'[^a-zA-Z0-9_\-]', '', key)
    return key

def clean_collection_name(name: str) -> str:
    # Replace spaces with underscores and remove invalid characters
    name = name.replace(' ', '_')
    name = re.sub(r'[^a-zA-Z0-9_]', '', name)
    # Ensure the name starts with a letter
    if not re.match(r'^[a-zA-Z]', name):
        name = 'col_' + name
    # Check if the name matches any AQL keywords and modify if necessary
    if name.upper() in AQL_KEYWORDS:
        name = f"Col_{name}"
    return name

def is_valid_collection_name(name):
    """Check if the collection name is valid according to ArangoDB's rules."""
    return re.match("^[a-zA-Z][a-zA-Z0-9_]*$", name) is not None

def create_graph_collection(graph_documents):
    for doc in graph_documents:
        nodes = doc.nodes
        relationships = doc.relationships

        for col in set(node.type for node in nodes):
            col = clean_collection_name(col)
            logging.debug(f"Attempting to create collection with name: {col}")
            if not is_valid_collection_name(col):
                logging.error(f"Invalid collection name: {col}")
                raise ValueError(f"Invalid collection name: {col}")

            if not db.has_collection(col):
                db.create_collection(col)

        for node in nodes:
            col = clean_collection_name(node.type)
            col = db.collection(col)
            node_id = clean_key(node.id)
            if not col.has(node_id):
                col.insert({
                    '_key': node_id,
                    **node.properties,
                })

        for rel in relationships:
            col = clean_collection_name(rel.type)
            logging.debug(f"Attempting to create edge collection with name: {col}")
            if not is_valid_collection_name(col):
                logging.error(f"Invalid edge collection name: {col}")
                raise ValueError(f"Invalid edge collection name: {col}")

            if not db.has_collection(col):
                db.create_collection(col, edge=True)

        for rel in relationships:
            col = clean_collection_name(rel.type)
            col = db.collection(col)
            source_id = clean_key(rel.source.id)
            target_id = clean_key(rel.target.id)
            edge_key = f"{source_id}_{target_id}"
            if not col.has(edge_key):
                col.insert({
                    '_key': edge_key,
                    '_from': f"{clean_collection_name(rel.source.type)}/{source_id}",
                    '_to': f"{clean_collection_name(rel.target.type)}/{target_id}",
                    **rel.properties,
                })

