---
icon: lucide/file-check
---

# Rules

_Rules_ are defined in `model_rules.toml` in your project's Django apps.

For Django Comb to consider a rule file, it must be _in the directory of an installed Django app_ --
typically, alongside a `models.py`.

## Example

```text hl_lines="6"
project/
  __init__.py
  blog/  <-- This must be in `INSTALLED_APPS`. 
    __init__.py
    models.py
    model_rules.toml
 ...
```

!!! note

    Model rules don't need to be defined in the same app as the models they refer to. 

Each rule definition should be in the form `[rule.my-rule-id]`. The second part of the TOML key (after the `.`)
is your rule's unique id. See below for examples.

## Rule types

### `no_inbound_foreign_keys`

Prevents other models from defining a `ForeignKey`, `OneToOneField` or `ManyToManyField` into a set of models.

| TOML Key              | Type                                  | Description                                                                                                                                                    |
|-----------------------|---------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `type`                | String                                | The rule type, must be `"no_inbound_foreign_keys"`.                                                                                                            |
| `models`              | String or Array of Strings            | The models to protect against inbound foreign keys pointing to them from other models, in the form  `app_label.ModelName`. Supports Unix shell-style wildcards. |
| `allowed`             | String or Array of Strings (optional) | Models that are allowed to point to `models`, in the form `app_label.ModelName`. Supports Unix shell-style wildcards.                                          |
| `silenced_violations` | String or Array of Strings (optional) | Functionally identical to `allowed`, but indicates undesirable dependencies. Supports Unix shell-style wildcards.                                    |

#### Example

```toml
# path/to/some_app/model_rules.toml

[rule.no-fks-to-blue-or-green]
type = "no_inbound_foreign_keys"
models = "some_app.*"  # All models in some_app.
allowed = [
    # It's okay for these models to have a foreign key
    # to the models above.
    "some_app.*",
    "another_app.Orange",
]
# Models listed here also point to the models above, but they shouldn't.
# Including them here suppresses violations in the same way as
# `allowed`, but indicates that the violation is technical debt
# rather than intentional design.
silenced_violations = "another_app.Purple"
```