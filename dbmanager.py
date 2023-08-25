import dataset
import logging
import uuid

# Set up logging for the module
logger = logging.getLogger(__name__)


def save_to_db(data, db_path):
    try:
        db = dataset.connect(f"sqlite:///{db_path}")

        for entity in data:
            schema = entity.get("schema")
            if schema:
                table_name = f"{schema}_entities"
                primary_key = str(uuid.uuid4())  # Generate a UUID as the primary key

                table = db.get_table(table_name) or db.create_table(table_name, primary_id="uuid")
                entity["uuid"] = primary_key  # Add the UUID to the entity dictionary
                table.upsert(entity, keys=["uuid"])  # Use the UUID as the primary key
                logger.info(f"Inserted '{schema}' into the database")
            else:
                logger.warning(f"Entity has no schema specified, skipping insertion: {entity}")
    except Exception as e:
        logger.error(f"Error while saving to the database: {e}")
