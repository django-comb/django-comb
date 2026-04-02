from __future__ import annotations
from django_comb.management.commands import lint_models
from textwrap import dedent

from . import _helpers


class TestLintModelsInvokeTask:
    def test_happy_path(self) -> None:
        result = _helpers.call_management_command("lint_models", "passing")

        assert result.returncode == 0
        assert result.stderr.decode() == dedent(
            """\
            ⚠️ warning: Unexpected key 'extra_key_one'
              --> rule.all in another_app/model_rules.toml

            ⚠️ warning: Unexpected key 'extra_key_two'
              --> rule.all in another_app/model_rules.toml

            ⚠️ warning: No rules found
              --> empty_rules_file_app/model_rules.toml

            😎 No violations in 5 models (checked 2 rules from 3 rule files).
            """
        )

    def test_detects_violations(self) -> None:
        result = _helpers.call_management_command("lint_models", "failing")

        assert result.returncode == lint_models.EXIT_CODE_VIOLATIONS_FOUND

        # Trim whitespace from the line endings.
        captured = "\n".join(
            line.rstrip() for line in result.stderr.decode().splitlines()
        )
        assert captured == dedent("""\
            ⚠️ warning: Unexpected key 'extra_key_one'
              --> rule.all in another_app/model_rules.toml

            ⚠️ warning: Unexpected key 'extra_key_two'
              --> rule.all in another_app/model_rules.toml

            ⚠️ warning: No rules found
              --> empty_rules_file_app/model_rules.toml

            ❌ no_inbound_foreign_keys: another_app.Orange.blue is a ForeignKey to some_app.Blue
              --> Violates rule blue-green in failing_app/model_rules.toml
              --> Field defined in another_app/models.py

            ❌ no_inbound_foreign_keys: another_app.Orange.greens is a ManyToManyField to some_app.Green
              --> Violates rule blue-green in failing_app/model_rules.toml
              --> Field defined in another_app/models.py

            ❌ no_inbound_foreign_keys: some_app.Green.blue is a ForeignKey to some_app.Blue
              --> Violates rule blue-green in failing_app/model_rules.toml
              --> Field defined in some_app/models.py

            ❌ no_inbound_foreign_keys: some_app.Green.blues is a ManyToManyField to some_app.Blue
              --> Violates rule blue-green in failing_app/model_rules.toml
              --> Field defined in some_app/models.py

            ❌ no_inbound_foreign_keys: another_app.Purple.blue is a OneToOneField to some_app.Blue
              --> Violates rule blue-green-no-arrays in failing_app/model_rules.toml
              --> Field defined in another_app/models.py

            ❌ no_inbound_foreign_keys: another_app.Purple.greens is a ManyToManyField to some_app.Green
              --> Violates rule blue-green-no-arrays in failing_app/model_rules.toml
              --> Field defined in another_app/models.py

            ❌ no_inbound_foreign_keys: another_app.Purple.blue is a OneToOneField to some_app.Blue
              --> Violates rule blue-green-wildcards in failing_app/model_rules.toml
              --> Field defined in another_app/models.py

            ❌ no_inbound_foreign_keys: another_app.Purple.greens is a ManyToManyField to some_app.Green
              --> Violates rule blue-green-wildcards in failing_app/model_rules.toml
              --> Field defined in another_app/models.py

            🙁 8 violations in 5 models (checked 5 rules from 4 rule files).""")

    def test_malformed_toml(self) -> None:
        result = _helpers.call_management_command("lint_models", "malformed_toml")

        assert result.returncode == lint_models.EXIT_CODE_ABNORMAL
        assert result.stderr.decode() == dedent(
            """\
            Invalid rule file malformed_toml_app/model_rules.toml:
            - Malformed TOML: Cannot declare ('rule', 'duplicate-id') twice (at line 5, column 19)
            Aborted.
            """
        )

    def test_invalid_config(self) -> None:
        result = _helpers.call_management_command("lint_models", "invalid")

        assert result.returncode == lint_models.EXIT_CODE_ABNORMAL
        assert result.stderr.decode() == dedent(
            """\
            Invalid rule file invalid_app/model_rules.toml:
            - Missing rule type (in rule.missing-type)
            - Unknown rule type 'nonexistent' (in rule.nonexistent-type)
            - Missing key 'models' (in rule.missing-required-field)
            - models: expression 'nonexistent_app.Violet' did not match any installed models (in rule.nonexistent-apps)
            - allowed: expression 'nonexistent_app.Indigo' did not match any installed models (in rule.nonexistent-apps)
            - silenced_violations: expression 'nonexistent_app.Pink' did not match any installed models (in rule.nonexistent-apps)
            - models: expression 'some_app.NonExistentModelOne' did not match any installed models (in rule.nonexistent-models)
            - allowed: expression 'some_app.NonExistentModelTwo' did not match any installed models (in rule.nonexistent-models)
            - silenced_violations: expression 'some_app.NonExistentModelThree' did not match any installed models (in rule.nonexistent-models)
            - models: must be a String or Array of Strings (in rule.model-expression-wrong-type)
            - allowed: must be a String or Array of Strings (in rule.model-expression-wrong-type)
            Aborted.
            """
        )
