from django.db import models


from Core.Producers.models import Producer
from Core.Studio.models import Studio


class Movie(models.Model):
    title = models.CharField(max_length=255, unique=True)
    year = models.PositiveIntegerField()
    winner = models.BooleanField(default=False)
    producer = models.ManyToManyField(Producer, related_name='movies')
    studio = models.ManyToManyField(Studio, related_name='movies')

    def __str__(self):
        return self.title
