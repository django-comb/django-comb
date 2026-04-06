---
icon: lucide/terminal
---

# `get_model_rules`

To view the discovered model rules as JSON, run the `get_model_rules` management command:

```text
$ python manage.py get_model_rules
[
  {
    "id": "all",
    "app_label": "another_app",
    "type": "no_inbound_foreign_keys",
    "models": [
      "some_app.*"
    ],
    "allowed": [
      "some_app.*",
      "another_app.Pur*"
    ],
    "silenced_violations": [
      "another_*.Orange"
    ],
    "extra_key_one": "foo",
    "extra_key_two": "bar"
  },
  {
    "id": "some-app-yellow",
    "app_label": "some_app",
    "type": "no_inbound_foreign_keys",
    "models": [
      "some_app.Yellow"
    ]
  }
]
```

This can be useful for building secondary tooling that tracks, say, the number of `silenced_violations` over time.