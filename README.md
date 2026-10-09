\# Customer Name \& Entity Extractor



\## 1. Project Overview



Customer Name \& Entity Extractor is a Python-based Natural Language Processing (NLP) application that extracts important entities and structured information from unstructured text.



The application combines spaCy Named Entity Recognition (NER) with Regular Expressions (Regex) to identify both standard NLP entities and structured entities such as email addresses, phone numbers, URLs, percentages, monetary values, temperatures, and quantities.



The extracted information is normalized, validated, and exported into JSON and CSV formats.



\---



\## 2. Problem Statement



Important information is often stored inside unstructured text such as emails, documents, customer messages, reports, and notes.



Manually identifying names, organizations, locations, dates, contact information, and other structured information can be time-consuming.



This project automates the extraction process using NLP and pattern-based techniques.



\---



\## 3. Objectives



The main objectives of this project are:



\- Extract named entities from unstructured text.

\- Identify people, organizations, locations, dates, times, and events.

\- Extract structured information using regular expressions.

\- Normalize extracted entities.

\- Remove duplicate entities.

\- Validate extracted data.

\- Export results into JSON format.

\- Export results into CSV format.

\- Create a reusable NLP extraction pipeline.



\---



\## 4. Key Features



\### NLP-based Entity Extraction



The project uses spaCy Named Entity Recognition to identify entities such as:



\- PERSON

\- ORG

\- GPE

\- EVENT

\- DATE

\- TIME

\- MONEY

\- QUANTITY

\- CARDINAL

\- PERCENT



\### Regex-based Extraction



Regular Expressions are used to identify:



\- Email addresses

\- Phone numbers

\- URLs

\- Percentages

\- Temperatures

\- Quantities

\- Monetary values



\### Entity Normalization



The project cleans extracted entities by:



\- Removing unnecessary whitespace.

\- Standardizing entity labels.

\- Removing duplicate entities.



\### Entity Validation



Each entity is checked for:



\- Required fields.

\- Valid text.

\- Valid labels.

\- Valid character positions.



\### Data Export



Results can be exported to:



\- JSON

\- CSV



\---



\## 5. Technologies Used



| Technology | Purpose |

|---|---|

| Python | Core programming language |

| spaCy | NLP and Named Entity Recognition |

| Regular Expressions | Structured entity extraction |

| pandas | CSV data processing |

| JSON | Structured output |

| pathlib | File and path management |

| pytest | Unit testing |



\---



\## 6. Project Architecture



The project follows a modular architecture:



```text

Input Text

&#x20;   |

&#x20;   v

spaCy Entity Extraction

&#x20;   |

&#x20;   v

Regex Entity Extraction

&#x20;   |

&#x20;   v

Combine Entities

&#x20;   |

&#x20;   v

Entity Normalization

&#x20;   |

&#x20;   v

Duplicate Removal

&#x20;   |

&#x20;   v

Entity Validation

&#x20;   |

&#x20;   v

JSON / CSV Export



\## 6. Project Structure


Customer Name \& Entity Extractor/

│

├── data/

│   └── sample\_input.txt

│

├── output/

│   ├── extracted\_entities.json

│   └── extracted\_entities.csv

│

├── src/

│   ├── \_\_init\_\_.py

│   ├── extractor.py

│   ├── regex\_extractor.py

│   ├── normalizer.py

│   ├── validator.py

│   └── exporter.py

│

├── tests/

│   └── test\_extractor.py

│

├── main.py

├── requirements.txt

├── README.md

└── .gitignore

