from __future__ import annotations

import json
from collections.abc import Mapping
from importlib import resources

import jsonschema_rs
import pytest
import pydantic.json_schema

from scripts import generate_model_rules_schema


@pytest.fixture
def schema() -> pydantic.json_schema.JsonSchemaValue:
    """
    Return the schema shipped in the package.
    """
    schema_path = resources.files("django_comb").joinpath("model_rules.schema.json")
    with schema_path.open(encoding="utf-8") as schema_file:
        return json.load(schema_file)


@pytest.fixture
def validator(
    schema: pydantic.json_schema.JsonSchemaValue,
) -> jsonschema_rs.Draft202012Validator:
    """
    Check the schema and return its Draft 2020-12 validator.
    """
    jsonschema_rs.meta.validate(schema)
    return jsonschema_rs.Draft202012Validator(schema)


class TestModelRulesSchema:
    @pytest.mark.parametrize(
        "expressions",
        [
            "some_app.Model",
            "some_app.*",
            ["some_app.*", "another_app.Model"],
            ["some_app.Model", "some_app.Model"],
            [],
        ],
    )
    def test_accepts_model_expressions(
        self,
        validator: jsonschema_rs.Draft202012Validator,
        expressions: str | list[str],
    ) -> None:
        data = {
            "rule": {
                "my-rule": {
                    "type": "no_inbound_foreign_keys",
                    "models": expressions,
                    "allowed": expressions,
                    "silenced_violations": expressions,
                }
            }
        }

        validator.validate(data)

    @pytest.mark.parametrize("data", [{}, {"rule": {}}])
    def test_accepts_empty_rule_files(
        self, validator: jsonschema_rs.Draft202012Validator, data: Mapping[str, object]
    ) -> None:
        validator.validate(data)

    @pytest.mark.parametrize(
        "rule",
        [
            {"models": "some_app.Model"},
            {"type": "no_inbound_foreign_keys"},
            {"type": "unknown", "models": "some_app.Model"},
            {"type": "no_inbound_foreign_keys", "models": 42},
            {"type": "no_inbound_foreign_keys", "models": ["some_app.Model", 42]},
            {"type": "no_inbound_foreign_keys", "models": {"some_app.Model": True}},
            {
                "type": "no_inbound_foreign_keys",
                "models": "some_app.Model",
                "allowed": False,
            },
            {
                "type": "no_inbound_foreign_keys",
                "models": "some_app.Model",
                "silenced_violations": [42],
            },
            {
                "type": "no_inbound_foreign_keys",
                "models": "some_app.Model",
                "alowed": [],  # Deliberate typo
            },
        ],
    )
    def test_rejects_invalid_rules(
        self, validator: jsonschema_rs.Draft202012Validator, rule: Mapping[str, object]
    ) -> None:
        with pytest.raises(jsonschema_rs.ValidationError):
            validator.validate({"rule": {"my-rule": rule}})

    @pytest.mark.parametrize(
        "data", [{"rules": {}}, {"rule": []}, {"rule": {"my-rule": []}}]
    )
    def test_rejects_invalid_structure(
        self, validator: jsonschema_rs.Draft202012Validator, data: Mapping[str, object]
    ) -> None:
        with pytest.raises(jsonschema_rs.ValidationError):
            validator.validate(data)

    def test_accepts_multiple_rules_with_optional_fields_omitted(
        self, validator: jsonschema_rs.Draft202012Validator
    ) -> None:
        data = {
            "rule": {
                "first": {
                    "type": "no_inbound_foreign_keys",
                    "models": "some_app.Model",
                },
                "second": {
                    "type": "no_inbound_foreign_keys",
                    "models": ["another_app.*"],
                },
            }
        }

        validator.validate(data)


class TestGenerateSchema:
    def test_matches_published_schema(
        self, schema: pydantic.json_schema.JsonSchemaValue
    ) -> None:
        generated_schema = generate_model_rules_schema.generate_schema()

        assert schema == generated_schema
