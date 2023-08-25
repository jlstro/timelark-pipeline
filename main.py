import os
import logging
from confection import registry, Config
from file_reader import read_text_from_files
from extractor import extract_entities
from alephutil import enrich_entities
from dbmanager import save_to_db
from glob import glob

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Load configuration from disk
config_file = Config().from_disk("./config.cfg")
config = registry.resolve(config_file)
# Access configuration values
db_path = config['paths']['db']
files_path = config['paths']['files']
aleph_host = config['aleph']['host']
collections = list[config['aleph']['collections']]
# Read API key from environment variable
api_key = os.environ.get("ALEPH_API_KEY")
# create aleph_config variable for easier handling
aleph_config = {"host":aleph_host, "api_key":api_key, "collections":collections}

# Check for None and log warnings if needed
missing_values = []
if db_path is None:
    missing_values.append("db_path")
if files_path is None:
    missing_values.append("files_path")
if aleph_host is None:
    missing_values.append("aleph_host")
if api_key is None:
    missing_values.append("api_key")

if missing_values:
    logging.warning("The following configuration values are missing or None: %s", ", ".join(missing_values))


if __name__ == "__main__":
    logging.info("Starting the data pipeline")

    # Use glob to get a list of all text files in the specified folder
    text_files = glob(files_path+"/*.txt")

    logging.info(f"Found {len(text_files)} text files to process")

    for txt in text_files:
        logging.info(f"Processing text file: {txt}")
        
        # Read text from the file
        text = read_text_from_files(txt)
        
        # Extract entities from the text
        entities = extract_entities(text)
        
        enriched_entities = []
        if entities:
            # Enrich entities using Aleph API
            for entity in entities: 
                enriched_entity = enrich_entities(entity, aleph_config)
                enriched_entities.append(enriched_entity)
        
        # Save enriched entities to the database
        save_to_db(enriched_entities, db_path)

        logging.info(f"Processed and saved data from {txt}")

    logging.info("Data pipeline completed")
