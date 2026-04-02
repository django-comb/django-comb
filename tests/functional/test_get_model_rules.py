import json
import pathlib
from . import _helpers

ASSETS_DIR = pathlib.Path(__file__).parent.parent / "assets"
TEST_PROJECT_DIR = ASSETS_DIR / "django_comb_project"


class TestGetModelRules:
    def test_returns_rules_as_json(self) -> None:
        result = _helpers.call_management_command("get_model_rules", "passing")

        assert result.returncode == 0
        rules_data = json.loads(result.stdout.decode())
        assert rules_data == [
            {
                "id": "all",
                "app_label": "another_app",
                "type": "no_inbound_foreign_keys",
                "models": ["some_app.*"],
                "allowed": ["some_app.*", "another_app.Pur*"],
                "silenced_violations": ["another_*.Orange"],
                "extra_key_one": "foo",
                "extra_key_two": "bar",
            },
            {
                "id": "some-app-yellow",
                "app_label": "some_app",
                "type": "no_inbound_foreign_keys",
                "models": ["some_app.Yellow"],
            },
        ]
