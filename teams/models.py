from django.db import models


class Team(models.Model):
    """Model for Team object"""

    name = models.CharField(max_length=50)
