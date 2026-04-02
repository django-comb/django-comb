from ._base import COMMON_INSTALLED_APPS

# Required for bootstrap.
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

INSTALLED_APPS = COMMON_INSTALLED_APPS + ("django_comb_project.failing_app",)
