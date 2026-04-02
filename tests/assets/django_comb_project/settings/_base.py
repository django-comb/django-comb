COMMON_INSTALLED_APPS = (
    "django_comb",
    "django_comb_project.some_app",
    "django_comb_project.another_app",
    # A rules file without any rules in will warn, not error.
    "django_comb_project.empty_rules_file_app",
)
