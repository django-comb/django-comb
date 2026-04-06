# Contributing

We welcome contributions to Django Comb.

## Bug reports

Report a bug by [opening a Github issue](https://github.com/django-comb/django-comb/issues/new).

## Feature requests and feedback

Send feedback or request a new feature by [opening a Github issue](https://github.com/django-comb/django-comb/issues/new).

## Submitting pull requests

Before spending time working on a pull request, we highly recommend filing a Github issue and engaging with the
project maintainer to align on the direction you're planning to take. This can save a lot of your
precious time!

This doesn't apply to trivial pull requests such as spelling corrections.

## Development

### System prerequisites

Make sure these are installed first.

- [git](https://github.com/git-guides/install-git)
- [uv](https://docs.astral.sh/uv/#installation)
- [just](https://just.systems/man/en/packages.html)

### Setup

You don't need to activate or manage a virtual environment - this is taken care in the background of by `uv`.

1. Fork [django-comb](https://github.com/django-comb/django-comb)
   (look for the "Fork" button).
2. Clone your fork locally:

    ```console
    git clone git@github.com:your_name_here/django-comb.git
    ```

3. Change into the directory you just cloned:

    ```console
    cd django-comb
    ```

4. Set up pre-commit. (Optional, but recommended.):

    ```console
    just install-precommit
    ```

You will now be able to run commands prefixed with `just`, providing you're in the `django-comb` directory.
To see available commands, run `just`.

### Formatting code

```console
just format
```

### Running linters

```console
just lint
```

### Running tests

When you're developing a feature, you'll probably want to run tests quickly, using just the latest supported Python version:

```console
just test
```

You can also pass a specific Python version, e.g. `just test --python=3.13`.

If you want to invoke pytest directly, e.g. to run a specific test, just use `uv run pytest`, e.g.:

```console
uv run pytest tests/functional/test_lint_models.py
```

Finally, you can run all the tests under all supported Python versions with `just test-all`. This gives a more complete
picture of whether the changes are compatible with all supported versions. Additionally, it will run tests under the
*lowest* versions of dependencies specified in `pyproject.toml`, with the lowest supported Python version. 

### Building documentation

To view docs locally: 

```console
just serve-docs
```

## Releasing to Pypi

(Only maintainers can do this.)

1. Choose a new version number (based on [semver](https://semver.org/)).
2. `git pull origin main`
3. Update `docs/release_notes.md` with the new version number.
4. Update the `__version__` variable in `src/django_comb/__init__.py` with the new version number.
5. Update `project.version` in `pyproject.toml` with the new version number.
6. `git commit -am "Release v{new version number"`
7. `git push`
8. Wait for tests to pass on CI.
9. `git tag v{new version number}`
10. `git push --tags`
11. This should kick start the Github `release` workflow which releases the project to PyPI.