---
icon: lucide/download
---
    
# Installation

Assuming a pre-existing Django project:

## 1. Install `django-comb`

Install `django-comb` using your favorite package manager.
You probably only need it as a dev dependency.

E.g.:

```
uv add --dev django-comb
```

## 2. Add it to `INSTALLED_APPS`

```python hl_lines="4"
# myproject/settings/dev.py

INSTALLED_APPS = [
   "django_comb",
   ...
]
```

You can now run the included management commands.