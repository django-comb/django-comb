---
icon: lucide/terminal
---

# `lint_models`

The `lint_models` management command checks your models are following all the [rules](../rules.md).

It's designed to be run in CI.

```text
python manage.py lint_models
```

## Exit codes

`lint_models` exits with the following status codes:

- `0` if no violations were found.
- `1` if violations were found.
- `2` if it terminates abnormally, e.g. due to invalid configuration.

