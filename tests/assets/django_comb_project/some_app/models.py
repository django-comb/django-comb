from __future__ import annotations

from django.db import models


class Blue(models.Model):
    pass


class Green(models.Model):
    blue = models.ForeignKey(Blue, on_delete=models.CASCADE)
    blues = models.ManyToManyField(Blue, related_name="other_blues")


class Yellow(models.Model):
    blue = models.ForeignKey(Blue, on_delete=models.CASCADE)
    greens = models.ManyToManyField(Green)
