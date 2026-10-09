import re


class RegexEntityExtractor:
    """
    Extract structured entities using regular expressions.
    """

    def extract_entities(self, text):
        entities = []

        patterns = {
            # Email addresses
            "EMAIL": (
                r"\b[A-Za-z0-9._%+-]+"
                r"@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
            ),

            # Web URLs
            "URL": r"https?://[^\s]+",

            # International and local phone numbers
            "PHONE": (
                r"(?<![\w.])"
                r"(?!\d{1,3}(?:\.\d{1,3}){3}(?!\d))"
                r"(?:\+?\d[\d\s().-]{8,}\d)"
                r"(?![\w.])"	
            ),

            # Percentage values
            "PERCENTAGE": (
                r"\b\d+(?:\.\d+)?%"
            ),

            # Temperature values
            "TEMPERATURE": (
                r"\b\d+(?:\.\d+)?\s?°[CF]\b"
            ),

            # Quantities with common units
            "QUANTITY": (
                r"\b\d+(?:\.\d+)?\s?"
                r"(?:kilograms?|kg|grams?|g|"
                r"liters?|litres?|meters?|metres?|"
                r"centimeters?|centimetres?|cm|"
                r"kilometers?|kilometres?|km|"
                r"milligrams?|mg|milliliters?|millilitres?|ml)"
                r"\b"
            ),

            # Currency values
            "MONEY": (
                r"(?:₹|\$|€|£)\s?"
                r"\d+(?:,\d{3})*(?:\.\d+)?"
            ),

            # IPv4 addresses
            "IP_ADDRESS": (
                r"\b"
                r"(?:\d{1,3}\.){3}\d{1,3}"
                r"\b"
            ),

            # Common postal/PIN codes
            "POSTAL_CODE": (
                r"(?<!\d)"
                r"\d{5,6}"
                r"(?!\d)"
            ),

            # Times such as 10:30 AM or 18:45
            "TIME": (
                r"\b"
                r"(?:[01]?\d|2[0-3]):[0-5]\d"
                r"(?:\s?[AP]M)?"
                r"\b"
            ),

            # Hashtags
            "HASHTAG": (
                r"(?<!\w)"
                r"#[A-Za-z0-9_]+"
            ),

            # Social-media style usernames
            "USERNAME": (
                r"(?<!\w)"
                r"@[A-Za-z0-9_]+"
            ),
        }

        for label, pattern in patterns.items():
            matches = re.finditer(
                pattern,
                text,
                flags=re.IGNORECASE
            )

            for match in matches:
                entities.append(
                    {
                        "text": match.group(),
                        "label": label,
                        "start": match.start(),
                        "end": match.end(),
                        "source": "Regex"
                    }
                )

        return entities