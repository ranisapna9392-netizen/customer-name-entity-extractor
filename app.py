
import streamlit as st
import pandas as pd

from src.entity_corrector import EntityCorrector
from src.extractor import SpacyEntityExtractor
from src.regex_extractor import RegexEntityExtractor
from src.normalizer import EntityNormalizer
from src.validator import EntityValidator
from src.exporter import EntityExporter


st.set_page_config(
    page_title="Customer Name & Entity Extractor",
    page_icon="🔎",
    layout="wide"
)

st.title("🔎 Customer Name & Entity Extractor")

st.write(
    "Enter any text to extract names, organizations, "
    "locations, dates, contact details, numbers, and more."
)

# User input
user_text = st.text_area(
    "Enter your text here",
    height=250,
    placeholder=(
        "Example: Sapna Rani works at Microsoft "
        "in Bengaluru, India. Contact her at "
        "sapna@example.com."
    ),
    key="input_text"
)

# Buttons
col1, col2 = st.columns(2)

with col1:
    extract_clicked = st.button(
        "🔍 Extract Entities",
        type="primary",
        use_container_width="stretch"
    )

with col2:
    clear_clicked = st.button(
        "🗑️ Clear",
        use_container_width="stretch"
    )

if clear_clicked:
    st.session_state["input_text"] = ""
    st.session_state.pop("entities", None)
    st.rerun()

if extract_clicked:
    if not user_text.strip():
        st.warning("Please enter some text first.")

    else:
        try:
            with st.spinner("Extracting entities..."):

                # spaCy extraction
                spacy_extractor = SpacyEntityExtractor()
                spacy_entities = (
                    spacy_extractor.extract_entities(user_text)
                )

                # Regex extraction
                regex_extractor = RegexEntityExtractor()
                regex_entities = (
                    regex_extractor.extract_entities(user_text)
                )

                # Combine entities
                all_entities = (
                    spacy_entities + regex_entities
                )

                # Correct labels
                corrector = EntityCorrector()
                corrected_entities = (
                    corrector.correct_entities(all_entities)
                )

                # Remove duplicates
                normalizer = EntityNormalizer()
                unique_entities = (
                    normalizer.remove_duplicates(
                        corrected_entities
                    )
                )

                # Validate entities
                validator = EntityValidator()
                valid_entities = (
                    validator.validate_entities(unique_entities)
                )

                # Store results for display
                st.session_state["entities"] = valid_entities

                # Export files
                exporter = EntityExporter()
                exporter.export_json(
                    valid_entities,
                    "output/extracted_entities.json"
                )
                exporter.export_csv(
                    valid_entities,
                    "output/extracted_entities.csv"
                )

        except Exception as e:
            st.error(f"Extraction failed: {e}")

if "entities" in st.session_state:
    entities = st.session_state["entities"]

    st.subheader("Extraction Results")

    st.metric("Total Entities Found", len(entities))

    if entities:
        df = pd.DataFrame(entities)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.subheader("Download Results")

        col1, col2 = st.columns(2)

        with col1:
            st.download_button(
                "Download CSV",
                data=df.to_csv(index=False).encode("utf-8"),
                file_name="extracted_entities.csv",
                mime="text/csv",
                use_container_width=True
            )

        with col2:
            st.download_button(
                "Download JSON",
                data=pd.Series(entities).to_json(
                    orient="values",
                    force_ascii=False,
                    indent=2
                ),
                file_name="extracted_entities.json",
                mime="application/json",
                use_container_width=True
            )

    else:
        st.info("No entities were detected in the supplied text.")