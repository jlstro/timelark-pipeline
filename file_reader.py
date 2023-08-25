import logging

# Set up logging for the module
logger = logging.getLogger(__name__)

def read_text_from_files(file_path):
    """
    Reads text from a file.

    Args:
        file_path (str): Path to the text file.

    Returns:
        str: Contents of the text file.
    """
    try:
        logger.info("Reading text from file: %s", file_path)
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()
            logger.info("Read text from file: %s", file_path)
            return text
    except Exception as e:
        logger.error("Error reading file %s: %s", file_path, e)
        raise RuntimeError(f"Error reading file {file_path}: {e}")
