import nox
import nox_uv

nox.options.default_venv_backend = "uv"

PYPROJECT = nox.project.load_toml("pyproject.toml")
PYTHON_VERSIONS = nox.project.python_versions(PYPROJECT)
EARLIEST_PYTHON = PYTHON_VERSIONS[0]


@nox_uv.session(
    python=PYTHON_VERSIONS,
    uv_groups=["dev"],
)
def test_each_python_version(session: nox.Session) -> None:
    session.run("pytest")


@nox.session(python=[EARLIEST_PYTHON])
def test_earliest_dependencies(session: nox.Session) -> None:
    """
    Try to detect any compatibility issues with lower bounds of our dependencies.

    We run the tests on the earliest version of Python and use the lowest-direct resolution
    strategy to install the lowest direct dependencies listed in pyproject.toml.
    """
    session.install("uv")

    # We can't use nox_uv for this one, nor `uv run`, as it will overwrite the project's uv.lock file.
    # Instead we use uv to install the lowest dependencies into the virtualenv provided by nox.
    session.run(
        "uv",
        "pip",
        "install",
        ".",
        "--group",
        "dev",
        "--resolution=lowest-direct",
        env={"VIRTUAL_ENV": session.virtualenv.location},
    )

    session.run("pytest")
