class EntityNormalizer:
    """
    Clean, normalize, remove duplicate entities,
    and resolve overlapping entity spans.
    """

    LABEL_MAPPING = {
        "PERSON": "PERSON",
        "GPE": "LOCATION",
        "LOC": "LOCATION",
        "NORP": "LOCATION",
        "ORG": "ORGANIZATION",
        "EVENT": "EVENT",
        "DATE": "DATE",
        "TIME": "TIME",
        "CARDINAL": "NUMBER",
        "MONEY": "MONEY",
        "PERCENT": "PERCENTAGE",
        "PERCENTAGE": "PERCENTAGE",
        "QUANTITY": "QUANTITY",
        "EMAIL": "EMAIL",
        "URL": "URL",
        "PHONE": "PHONE",
        "TEMPERATURE": "TEMPERATURE",
        "IP_ADDRESS": "IP_ADDRESS",
        "POSTAL_CODE": "POSTAL_CODE",
        "HASHTAG": "HASHTAG",
        "USERNAME": "USERNAME"
    }


    ENTITY_CORRECTIONS = {
        "nestle": "ORGANIZATION",
        "apple": "ORGANIZATION"
    }

    def normalize_entity(self, entity):
        normalized_entity = entity.copy()

        normalized_entity["text"] = (
            normalized_entity["text"]
            .strip()
            .replace("\n", " ")
        )

        raw_label = (
            normalized_entity["label"]
            .strip()
            .upper()
        )
        
        normalized_label = self.LABEL_MAPPING.get(
            
            raw_label,
            raw_label
        )

        normalized_entity["label"] = (
            self.ENTITY_CORRECTIONS.get(
                normalized_entity["text"].lower(),
                normalized_label
            )
        )

        return normalized_entity

    def remove_duplicates(self, entities):
        normalized_entities = [
            self.normalize_entity(entity)
            for entity in entities
        ]

        # Sort by start position and then by
        # longest entity first.
        normalized_entities.sort(
            key=lambda entity: (
                entity["start"],
                -(entity["end"] - entity["start"])
            )
        )

        unique_entities = []

        for entity in normalized_entities:
            is_duplicate_or_overlap = False

            for existing in unique_entities:

                # Check whether the two spans overlap.
                if (
                    entity["start"] < existing["end"]
                    and entity["end"] > existing["start"]
                ):
                    is_duplicate_or_overlap = True
                    break

            if not is_duplicate_or_overlap:
                unique_entities.append(entity)

        # Return entities in their original text order.
        unique_entities.sort(
            key=lambda entity: entity["start"]
        )

        return unique_entities