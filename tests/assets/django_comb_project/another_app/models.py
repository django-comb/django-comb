from __future__ import annotations

from django.db import models

from django_comb_project.some_app import models as some_models


class Purple(models.Model):
    blue = models.OneToOneField(some_models.Blue, on_delete=models.CASCADE)
    greens = models.ManyToManyField("some_app.Green")


class Orange(models.Model):
    blue = models.ForeignKey(some_models.Blue, on_delete=models.CASCADE)
    greens = models.ManyToManyField("some_app.Green")
