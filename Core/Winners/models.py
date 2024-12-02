from django.db import models


from Core.Movies.models import Movie


class Winner(models.Model):
    award = models.CharField(max_length=255)
    year = models.PositiveIntegerField()
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name='winners_movies'
    )

    def __str__(self):
        return f"{self.award} ({self.year}) for {self.movie.title}"
