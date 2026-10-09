
from src.entity_corrector import EntityCorrector
from src.extractor import SpacyEntityExtractor
from src.regex_extractor import RegexEntityExtractor
from src.normalizer import EntityNormalizer
from src.validator import EntityValidator


# ---------------------------------------------------------
# spaCy Entity Extraction Tests
# ---------------------------------------------------------

def test_spacy_extraction():
    extractor = SpacyEntityExtractor()

    text = "Sapna Rani works at Nestle in Mumbai."

    entities = extractor.extract_entities(text)

    assert isinstance(entities, list)

    assert any(
        entity["text"] == "Sapna Rani"
        and entity["label"] == "PERSON"
        for entity in entities
    )


# ---------------------------------------------------------
# Regex Extraction Tests
# ---------------------------------------------------------

def test_regex_email_extraction():
    extractor = RegexEntityExtractor()

    text = "Contact me at sapna@example.com"

    entities = extractor.extract_entities(text)

    assert any(
        entity["text"] == "sapna@example.com"
        and entity["label"] == "EMAIL"
        for entity in entities
    )


def test_regex_phone_extraction():
    extractor = RegexEntityExtractor()

    text = "My phone number is +91-9876543210"

    entities = extractor.extract_entities(text)

    assert any(
        entity["text"] == "+91-9876543210"
        and entity["label"] == "PHONE"
        for entity in entities
    )


def test_ip_address_extraction():
    extractor = RegexEntityExtractor()

    text = "Server IP is 192.168.1.100"

    entities = extractor.extract_entities(text)

    assert any(
        entity["text"] == "192.168.1.100"
        and entity["label"] == "IP_ADDRESS"
        for entity in entities
    )


def test_ip_address_not_detected_as_phone():
    extractor = RegexEntityExtractor()

    text = "Server IP is 192.168.1.100"

    entities = extractor.extract_entities(text)

    assert not any(
        entity["text"] == "192.168.1.100"
        and entity["label"] == "PHONE"
        for entity in entities
    )


def test_postal_code_extraction():
    extractor = RegexEntityExtractor()

    text = "My postal code is 122001"

    entities = extractor.extract_entities(text)

    assert any(
        entity["text"] == "122001"
        and entity["label"] == "POSTAL_CODE"
        for entity in entities
    )


def test_time_extraction():
    extractor = RegexEntityExtractor()

    text = "The meeting starts at 10:30 AM"

    entities = extractor.extract_entities(text)

    assert any(
        entity["text"] == "10:30 AM"
        and entity["label"] == "TIME"
        for entity in entities
    )


def test_hashtag_extraction():
    extractor = RegexEntityExtractor()

    text = "I love #Python and #ArtificialIntelligence"

    entities = extractor.extract_entities(text)

    assert any(
        entity["text"] == "#Python"
        and entity["label"] == "HASHTAG"
        for entity in entities
    )

    assert any(
        entity["text"] == "#ArtificialIntelligence"
        and entity["label"] == "HASHTAG"
        for entity in entities
    )


def test_username_extraction():
    extractor = RegexEntityExtractor()

    text = "Contact @sapna_rani"

    entities = extractor.extract_entities(text)

    assert any(
        entity["text"] == "@sapna_rani"
        and entity["label"] == "USERNAME"
        for entity in entities
    )


def test_unicode_money_extraction():
    extractor = RegexEntityExtractor()

    text = "The price is ₹ 80,000"

    entities = extractor.extract_entities(text)

    assert any(
        entity["text"] == "₹ 80,000"
        and entity["label"] == "MONEY"
        for entity in entities
    )


def test_unicode_temperature_extraction():
    extractor = RegexEntityExtractor()

    text = "The temperature is 28°C"

    entities = extractor.extract_entities(text)

    assert any(
        entity["text"] == "28°C"
        and entity["label"] == "TEMPERATURE"
        for entity in entities
    )


# ---------------------------------------------------------
# Entity Normalization Tests
# ---------------------------------------------------------

def test_normalization():
    normalizer = EntityNormalizer()

    entities = [
        {
            "text": "  Sapna Rani  ",
            "label": " person ",
            "start": 0,
            "end": 10
        }
    ]

    result = normalizer.remove_duplicates(entities)

    assert result[0]["text"] == "Sapna Rani"
    assert result[0]["label"] == "PERSON"


def test_duplicate_removal():
    normalizer = EntityNormalizer()

    entities = [
        {
            "text": "Mumbai",
            "label": "GPE",
            "start": 0,
            "end": 6
        },
        {
            "text": "Mumbai",
            "label": "GPE",
            "start": 0,
            "end": 6
        }
    ]

    result = normalizer.remove_duplicates(entities)

    assert len(result) == 1


def test_duplicate_span_removal():
    normalizer = EntityNormalizer()

    entities = [
        {
            "text": "25%",
            "label": "PERCENT",
            "start": 10,
            "end": 13
        },
        {
            "text": "25%",
            "label": "PERCENTAGE",
            "start": 10,
            "end": 13
        }
    ]

    result = normalizer.remove_duplicates(entities)

    assert len(result) == 1
    assert result[0]["text"] == "25%"


def test_overlapping_entity_removal():
    normalizer = EntityNormalizer()

    entities = [
        {
            "text": "80,000",
            "label": "MONEY",
            "start": 10,
            "end": 16
        },
        {
            "text": "₹80,000",
            "label": "MONEY",
            "start": 9,
            "end": 16
        }
    ]

    result = normalizer.remove_duplicates(entities)

    assert len(result) == 1
    assert result[0]["text"] == "₹80,000"


def test_entity_corrector_changes_mumbai_to_location():
    corrector = EntityCorrector()

    entity = {
        "text": "Mumbai",
        "label": "ORG",
        "start": 0,
        "end": 6,
        "source": "spaCy"
    }

    corrected = corrector.correct_entity(entity)

    assert corrected["label"] == "GPE"


def test_entity_corrector_changes_india_to_location():
    corrector = EntityCorrector()

    entity = {
        "text": "India",
        "label": "ORG",
        "start": 0,
        "end": 5,
        "source": "spaCy"
    }

    corrected = corrector.correct_entity(entity)

    assert corrected["label"] == "GPE"


def test_entity_corrector_changes_maharashtra_to_location():
    corrector = EntityCorrector()

    entity = {
        "text": "Maharashtra",
        "label": "ORG",
        "start": 0,
        "end": 11,
        "source": "spaCy"
    }

    corrected = corrector.correct_entity(entity)

    assert corrected["text"] == "Maharashtra"
    assert corrected["label"] == "GPE"


def test_entity_corrector_keeps_organization_unchanged():
    corrector = EntityCorrector()

    entity = {
        "text": "Apple",
        "label": "ORG",
        "start": 0,
        "end": 5,
        "source": "spaCy"
    }

    corrected = corrector.correct_entity(entity)

    assert corrected["label"] == "ORG"


def test_entity_corrector_preserves_entity_data():
    corrector = EntityCorrector()

    entity = {
        "text": "Maharashtra",
        "label": "ORG",
        "start": 10,
        "end": 21,
        "source": "spaCy"
    }

    corrected = corrector.correct_entity(entity)

    assert corrected["text"] == "Maharashtra"
    assert corrected["start"] == 10
    assert corrected["end"] == 21
    assert corrected["source"] == "spaCy"


def test_entity_corrector_multiple_entities():
    corrector = EntityCorrector()

    entities = [
        {
            "text": "Mumbai",
            "label": "GPE",
            "start": 0,
            "end": 6,
            "source": "spaCy"
        },
        {
            "text": "Maharashtra",
            "label": "ORG",
            "start": 8,
            "end": 19,
            "source": "spaCy"
        },
        {
            "text": "Apple",
            "label": "ORG",
            "start": 21,
            "end": 26,
            "source": "spaCy"
        }
    ]

    corrected = corrector.correct_entities(entities)

    assert corrected[0]["label"] == "GPE"
    assert corrected[1]["label"] == "GPE"
    assert corrected[2]["label"] == "ORG"
