import spacy


class SpacyEntityExtractor:
    """
    Extracts entities from text using spaCy's pre-trained model.
    """

    def __init__(self, model_name="en_core_web_sm"):
        self.nlp = spacy.load(model_name)

    def extract_entities(self, text):
        """
        Extract entities from the provided text.

        Args:
            text: Input text.

        Returns:
            A list of extracted entities.
        """

        doc = self.nlp(text)

        entities = []

        for entity in doc.ents:
            entities.append(
                {
                    "text": entity.text,
                    "label": entity.label_,
                    "start": entity.start_char,
                    "end": entity.end_char,
                    "source": "spaCy"
                }
            )

        return entities