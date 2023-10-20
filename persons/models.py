from django.db import models

from teams.models import Team


class Person(models.Model):
    """Model for Person object"""

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, related_name="members", null=True, blank=True)
