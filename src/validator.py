class EntityValidator:
    """
    Validate extracted entities.
    """

    REQUIRED_FIELDS = {
        "text",
        "label",
        "start",
        "end"
    }

    def validate_entity(self, entity):
        missing_fields = (
            self.REQUIRED_FIELDS
            - set(entity.keys())
        )

        if missing_fields:
            return False

        if not entity["text"].strip():
            return False

        if not entity["label"].strip():
            return False

        if entity["start"] < 0:
            return False

        if entity["end"] < entity["start"]:
            return False

        return True

    def validate_entities(self, entities):
        valid_entities = []

        for entity in entities:
            if self.validate_entity(entity):
                valid_entities.append(entity)

        return valid_entities