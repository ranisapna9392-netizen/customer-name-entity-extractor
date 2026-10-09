
from pathlib import Path

from src.entity_corrector import EntityCorrector
from src.extractor import SpacyEntityExtractor
from src.regex_extractor import RegexEntityExtractor
from src.normalizer import EntityNormalizer
from src.validator import EntityValidator
from src.exporter import EntityExporter


def read_input_file(file_path):
    """
    Read text from a file.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    return path.read_text(encoding="utf-8")


def main():
    input_file = "data/sample_input.txt"

    json_output = "output/extracted_entities.json"
    csv_output = "output/extracted_entities.csv"

    print("Reading input file...")

    text = read_input_file(input_file)

    print("Extracting entities using spaCy...")

    spacy_extractor = SpacyEntityExtractor()

    spacy_entities = (
        spacy_extractor.extract_entities(text)
    )

    print("Extracting entities using Regex...")

    regex_extractor = RegexEntityExtractor()

    regex_entities = (
        regex_extractor.extract_entities(text)
    )

    all_entities = (
        spacy_entities
        + regex_entities
    )

    print("Correcting entity labels...")

    corrector = EntityCorrector()

    corrected_entities = (
        corrector.correct_entities(
            all_entities
        )
    )

    print("Removing duplicates...")

    normalizer = EntityNormalizer()

    unique_entities = (
        normalizer.remove_duplicates(
            corrected_entities
        )
    )

    print("Validating entities...")

    validator = EntityValidator()

    valid_entities = (
        validator.validate_entities(
            unique_entities
        )
    )

    print("Exporting results...")

    exporter = EntityExporter()

    exporter.export_json(
        valid_entities,
        json_output
    )

    exporter.export_csv(
        valid_entities,
        csv_output
    )

    print("\nExtraction completed successfully.")

    print(
        f"Total entities found: {len(valid_entities)}"
    )

    print("\nExtracted Entities:")
    print("-" * 50)

    for entity in valid_entities:
        print(
            f"{entity['text']} -> {entity['label']}"
        )

    print("-" * 50)

    print(f"JSON output: {json_output}")
    print(f"CSV output: {csv_output}")


if __name__ == "__main__":
    main()

