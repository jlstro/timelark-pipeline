import spacy
import logging

# Set up logging for the module
logger = logging.getLogger(__name__)

# Load the larger spaCy model for entity recognition
nlp = spacy.load("en_core_web_lg")  # or en_core_web_md or sm

def extract_entities(text):
    """
    Extracts entities from the given text and filters for specific categories.

    Args:
        text (str): Input text to extract entities from.

    Returns:
        list: List of extracted entities.
    """
    try:
        logger.info("Extracting entities from text")
        doc = nlp(text)
        entities = []
        target_labels = ["LOC", "PERSON", "ORG", "GPE", "DATE", "EVENT"]
        for ent in doc.ents:
            if ent.label_ in target_labels:
                entities.append({"text": ent.text, "category": ent.label_})
        logger.info(f"Extracted {len(entities)} entities from text")
        return entities
    except Exception as e:
        logger.error(f"Error extracting entities: {e}")
        raise RuntimeError(f"Error extracting entities: {e}")
