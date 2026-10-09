class EntityCorrector:
    """
    Correct common entity misclassifications
    produced by the NER model.
    """

    LOCATION_ENTITIES = {
        "Maharashtra",
        "Mumbai",
        "India",
        "Paris",
        "France"
    }

    def correct_entity(self, entity):
        corrected_entity = entity.copy()

        text = corrected_entity["text"].strip()

        if text in self.LOCATION_ENTITIES:
            corrected_entity["label"] = "GPE"

        return corrected_entity

    def correct_entities(self, entities):
        return [
            self.correct_entity(entity)
            for entity in entities
        ]