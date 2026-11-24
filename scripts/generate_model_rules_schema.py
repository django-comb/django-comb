"""
Generate the published schema from Django Comb's Pydantic rule configurations.
"""

from __future__ import annotations

import json
from pathlib import Path

import pydantic.json_schema

from django_comb import _rule_files


SCHEMA_PATH = (
    Path(__file__).resolve().parents[1] / "src/django_comb/model_rules.schema.json"
)
SCHEMA_URL = "https://raw.githubusercontent.com/django-comb/django-comb/main/src/django_comb/model_rules.schema.json"


def generate_schema() -> pydantic.json_schema.JsonSchemaValue:
    """
    Return the editor schema generated from the registered rule configurations.
    """
    rule_schemas: list[pydantic.json_schema.JsonSchemaValue] = []
    for rule_type, config_class in sorted(
        _rule_files.RULE_CONFIG_CLASSES_BY_NAME.items()
    ):
        rule_schema = config_class.model_json_schema()
        # Rule types are dispatched before Pydantic validates the configuration.
        rule_schema["properties"]["type"] = {"const": rule_type}
        rule_schema["required"].append("type")
        # Runtime validation warns about unknown rule keys; editor validation
        # rejects them so misspelled optional fields are easy to spot.
        rule_schema["additionalProperties"] = False
        rule_schemas.append(rule_schema)

    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": SCHEMA_URL,
        "title": "Django Comb model rules",
        "description": (
            "Generated from Django Comb's Pydantic rule configurations. Model expression matching "
            "and relationship checks require Django Comb."
        ),
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "rule": {
                "type": "object",
                "additionalProperties": {"oneOf": rule_schemas},
            }
        },
    }


if __name__ == "__main__":
    with SCHEMA_PATH.open("w", encoding="utf-8") as schema_file:
        json.dump(generate_schema(), schema_file, indent=2)
        schema_file.write("\n")
