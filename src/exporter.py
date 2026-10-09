import json
from pathlib import Path

import pandas as pd


class EntityExporter:
    """
    Export entities into JSON and CSV.
    """

    def export_json(self, entities, output_path):
        output_path = Path(output_path)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with output_path.open(
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                entities,
                file,
                indent=4,
                ensure_ascii=False
            )

    def export_csv(self, entities, output_path):
        output_path = Path(output_path)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        dataframe = pd.DataFrame(entities)

        dataframe.to_csv(
            output_path,
            index=False,
            encoding="utf-8-sig"
        )