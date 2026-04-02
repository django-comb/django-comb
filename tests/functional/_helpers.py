import subprocess
import os
import sys
import pathlib


ASSETS_DIR = pathlib.Path(__file__).parent.parent / "assets"
TEST_PROJECT_DIR = ASSETS_DIR / "django_comb_project"


def call_management_command(
    command: str, settings_module: str
) -> subprocess.CompletedProcess:
    """
    Calls the supplied management command under a Django configuration.
    """
    amended_python_path = f"{ASSETS_DIR}:{os.environ.get('PYTHONPATH', '')}"

    return subprocess.run(
        [sys.executable, "manage.py", command],
        capture_output=True,
        cwd=TEST_PROJECT_DIR,
        env={
            "PYTHONPATH": amended_python_path,
            "DJANGO_SETTINGS_MODULE": f"django_comb_project.settings.{settings_module}",
            # Use a wide terminal to prevent us having to take wrapping into consideration.
            "COLUMNS": "150",
        },
    )
